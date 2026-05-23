# =========================================================================
# DEFINITION OF FLET STRUCTURAL TERMS & PROPERTIES
# =========================================================================
# * ft.Page         : The root window canvas workspace wrapper.
# * page.window     : Horizontal & vertical width layout frame dimensions.
# * ft.TabBar       : The navigation button strip placed at the top of the app.
# * ft.Tab          : An individual click element inside the TabBar (uses 'label').
# * ft.TabBarView   : The engine container that holds and slides your content pages.
# * ft.Container    : Block container used for application padding adjustments.
# * ft.Column       : Vertical UI layout organizer.
# * ft.Row          : Horizontal UI layout organizer.
# * ft.TextField    : Captured string text entry field.
# * page.update()   : Redraws the layout instantly when values shift.
# -------------------------------------------------------------------------
#   NEW STRUCTURAL ADDITIONS & INTEGRATED LAYOUT PROPERTIES
# -------------------------------------------------------------------------
# * ft.AppBar       : Top branding header bar displaying the system title.
# * ft.Dropdown     : Structural selection menu used for static criteria.
# * ft.Divider      : A thin visual rule line separating functional UI sections.
# * disabled=True   : Field property locking an element to read-only status.
# * expand=X        : Dynamic alignment property scaling items across rows/columns.
# * input_filter    : Enforcement ruleset matching input via regular expressions.
# * text_align      : Component alignment controller for textual data within fields.
# * vertical_alignment : Grid layout axis controller organizing grouped components.
# =========================================================================

import flet as ft
from BloodDonationSystem import BloodDonationDatabase, Donor
from datetime import datetime

def main(page: ft.Page):
    # App Frame Dimension Configurations (Matches window aspect ratios seen in screenshots)
    page.window_width = 500
    page.window_height = 850
    page.window_resizable = True
    
    # Theme Display Options
    page.title = "Blood Bank Core App"
    page.theme_mode = ft.ThemeMode.LIGHT 
    
    # Initialize connection to your MariaDB schema database engine
    db = BloodDonationDatabase(
        host="localhost",
        user="root",
        password="", 
        database="blood_donation_system_database"
    )

    # =========================================================================
    # TAB VIEW MODULE 1: DONOR REGISTRATION
    # =========================================================================
    reg_name = ft.TextField(label="Full Name", border_radius=10, width=380)

    # Age transformed into a matching, read-only TextField style layout
    reg_age_auto = ft.TextField(
        label="Age", 
        value="--", 
        disabled=True, 
        border_radius=10,
        text_align=ft.TextAlign.CENTER,
        expand=1
    )

    reg_consent = ft.Checkbox(
        label="Parental Consent Form Verified", 
        value=False,
        visible=False, # Hidden by default
        disabled=True
    )

    # Function that watches the text input and calculates age automatically
    def auto_calculate_age(e):
        current_text = (reg_birthdate.value or "").strip()
        
        # SMART DASH INJECTION
        if e.data and len(current_text) in [4, 7] and not current_text.endswith("-"):
            reg_birthdate.value = current_text + "-"
            reg_birthdate.cursor_position = len(reg_birthdate.value)
            current_text = reg_birthdate.value

        if len(current_text) == 10:
            try:
                birth_date = datetime.strptime(current_text, "%Y-%m-%d").date()
                today = datetime.now().date()
                calculated_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                
                if 0 <= calculated_age <= 120:
                    reg_age_auto.value = f"{calculated_age}"
                    
                    # 🌟 DYNAMIC LOGIC FOR 17-YEAR-OLDS
                    if calculated_age == 17:
                        reg_consent.visible = True
                        reg_consent.disabled = False
                    else:
                        reg_consent.visible = False
                        reg_consent.disabled = True
                        reg_consent.value = False # Reset if age changes away from 17
                else:
                    reg_age_auto.value = "Invalid"
                    reg_consent.visible = False
            except ValueError:
                reg_age_auto.value = "Error"
                reg_consent.visible = False
        else:
            reg_age_auto.value = "--"
            reg_consent.visible = False
            
        page.update()

    # The Birthdate field with the 'on_change' hook and number/dash filter attached
    reg_birthdate = ft.TextField(
        label="Birthdate (YYYY-MM-DD)", 
        hint_text="YYYY-MM-DD",
        border_radius=10,
        max_length=10,
        on_change=auto_calculate_age,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9\-]", replacement_string=""),
        expand=3
    )

    reg_weight = ft.TextField(label="Weight (kg)", border_radius=10, width=380)

    # Force the user keyboard/field entry system to only accept numerical digits
    reg_contact = ft.TextField(
        label="Contact Number", 
        max_length=11,
        border_radius=10,
        width=380,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string="")
    )
    
    reg_blood = ft.Dropdown(
        label="Blood Group Selection",
        border_radius=10,
        width=380,
        options=[
            ft.dropdown.Option("A+"), ft.dropdown.Option("A-"),
            ft.dropdown.Option("B+"), ft.dropdown.Option("B-"),
            ft.dropdown.Option("O+"), ft.dropdown.Option("O-"),
            ft.dropdown.Option("AB+"), ft.dropdown.Option("AB-"),
        ]
    )
    reg_output = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def process_registration(e):
        if not (reg_name.value and reg_birthdate.value and reg_weight.value and reg_contact.value and reg_blood.value):
            reg_output.value = "All fields are required!"
            reg_output.color = ft.Colors.RED_600 
            page.update()
            return
        
        contact_input = reg_contact.value.strip()
        birthdate_input = reg_birthdate.value.strip()
        
        if not (contact_input.isdigit() and len(contact_input) == 11):
            reg_output.value = "Registration Denied: Contact number must be exactly 11 digits!"
            reg_output.color = ft.Colors.RED_600
            page.update()
            return
        
        try:
            birth_date = datetime.strptime(birthdate_input, "%Y-%m-%d").date()
            today = datetime.now().date()
            calculated_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            new_donor = Donor(
                name=reg_name.value.strip(),
                age=calculated_age, 
                contact=contact_input, 
                blood_type=reg_blood.value,
                weight=float(reg_weight.value.strip())
            )
            if db.register_donor(new_donor):
                reg_output.value = f"Successfully registered: {new_donor.get_name()}"
                reg_output.color = ft.Colors.GREEN_700 
                
                # Clear out the text inputs
                reg_name.value = reg_birthdate.value = reg_weight.value = reg_contact.value = reg_blood.value = ""
                reg_age_auto.value = "--"
                
                load_live_inventory_records()
            else:
                reg_output.value = "Database storage execution rejected."
                reg_output.color = ft.Colors.RED_600
        except ValueError:
            reg_output.value = "Format Error! Age must be integer, Weight must be decimal."
            reg_output.color = ft.Colors.RED_600
        page.update()

    # Form components collected inside a strictly centered, uniform structural column
    registration_form_panel = ft.Column(
        [
            ft.Text("Register New Donor Entry", size=18, weight=ft.FontWeight.BOLD),
            reg_name, 
            ft.Row([
                reg_birthdate,
                reg_age_auto
            ], width=380, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
            
            reg_consent, # 🌟 ALSO ADD IT HERE so it renders below the Age/Birthdate row!
            
            reg_weight, 
            reg_contact, 
            reg_blood,
            ft.Row([
                ft.Button(content=ft.Text("Save Donor", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_900, on_click=process_registration)
            ], width=380, alignment=ft.MainAxisAlignment.CENTER),
            reg_output
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )

    register_layout = ft.Container(
        content=ft.Row([registration_form_panel], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.Alignment(0, -1) # 'scroll' keyword completely removed
    )

    # =========================================================================
    # TAB VIEW MODULE 2: ELIGIBILITY CHECKER
    # =========================================================================
    chk_age = ft.TextField(label="Enter Age", border_radius=10, width=380)
    chk_weight = ft.TextField(label="Enter Weight (kg)", border_radius=10, width=380)
    chk_months = ft.TextField(label="Months Since Last Donation", border_radius=10, width=380)
    chk_illness = ft.Dropdown(
        label="Any Current Illnesses?",
        value="No",
        border_radius=10,
        width=380,
        options=[ft.dropdown.Option("No"), ft.dropdown.Option("Yes")]
    )
    chk_output = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def verify_eligibility(e):
        try:
            age = int(chk_age.value.strip())
            weight = float(chk_weight.value.strip())
            months = int(chk_months.value.strip())
            has_illness = chk_illness.value == "Yes"

            is_eligible = (18 <= age <= 65) and (weight >= 50) and (months >= 3) and (not has_illness)

            if is_eligible:
                chk_output.value = "Status: ELIGIBLE TO DONATE BLOOD"
                chk_output.color = ft.Colors.GREEN_700
            else:
                chk_output.value = "Status: NOT ELIGIBLE\n(Must match: 18-65 yrs, >=50kg, >=3 months rest, healthy)"
                chk_output.color = ft.Colors.RED_ACCENT_700
                chk_output.italic = True
        except (ValueError, AttributeError):
            chk_output.value = "Please complete validation metrics with numeric figures."
            chk_output.color = ft.Colors.ORANGE_800
        page.update()

    eligibility_form_panel = ft.Column(
        [
            ft.Text("Medical Screening Matrix", size=18, weight=ft.FontWeight.BOLD),
            chk_age, chk_weight, chk_months, chk_illness,
            ft.Row([
                ft.Button(content=ft.Text("Verify", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_900, on_click=verify_eligibility)
            ], width=380, alignment=ft.MainAxisAlignment.CENTER),
            chk_output
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO # MOVED HERE
    )

    eligibility_layout = ft.Container(
        content=ft.Row([eligibility_form_panel], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.Alignment(0, -1)
    )

    # =========================================================================
    # TAB VIEW MODULE 3: BLOOD INVENTORY
    # =========================================================================
    inventory_list_view = ft.Column(spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=380)

    def load_live_inventory_records(e=None):
        inventory_list_view.controls.clear()
        
        from BloodDonationSystem import BloodInventory
        inv_manager = BloodInventory(db)
        stock_data = inv_manager.get_inventory_data()

        if not stock_data:
            inventory_list_view.controls.append(ft.Text("No inventory table records uncovered.", color=ft.Colors.RED_500))
            page.update()
            return

        inventory_list_view.controls.append(ft.Text("Available Blood Bank Storage Units:", size=18, weight=ft.FontWeight.BOLD))
        
        for b_type, units in stock_data.items():
            inventory_list_view.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"Blood Type: {b_type}", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{units} Units In-Stock", size=14, color=ft.Colors.GREEN_700 if units > 0 else ft.Colors.RED_600)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=12,
                    border_radius=8,
                    bgcolor=ft.Colors.GREY_100,
                    width=380
                )
            )
        page.update()

    inventory_form_panel = ft.Column(
        [
            inventory_list_view,
            ft.Row([
                ft.Button(content=ft.Text("Refresh Records", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLUE_GREY_700, on_click=load_live_inventory_records)
            ], width=380, alignment=ft.MainAxisAlignment.CENTER)
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO # MOVED HERE
    )

    inventory_layout = ft.Container(
        content=ft.Row([inventory_form_panel], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.Alignment(0, -1)
    )

    # =========================================================================
    # TAB VIEW MODULE 4: DATABASE ENGINE LOOKUP
    # =========================================================================
    search_input = ft.TextField(label="Search Parameter", hint_text="Name or Type (e.g. O+)", border_radius=10, width=380)
    search_mode = ft.Dropdown(
        label="Classification",
        value="Name",
        border_radius=10,
        width=380,
        options=[ft.dropdown.Option("Name"), ft.dropdown.Option("Blood Type")]
    )
    search_output_display = ft.Text(size=14, color=ft.Colors.BLACK)

    def handle_search_execution(e):
        query = search_input.value.strip()
        if not query:
            search_output_display.value = "Provide valid entry search details."
            page.update()
            return

        if search_mode.value == "Name":
            donor = db.search_by_name(query)
            if donor:
                search_output_display.value = (
                    f"Match Located:\n\n"
                    f"Name: {donor.get_name()}\n"
                    f"Age: {donor.get_age()}\n"
                    f"Contact Details: {donor.get_contact()}\n"
                    f"Blood Profile: {donor.get_blood_type()}\n"
                    f"Mass: {donor.get_weight()} kg"
                )
            else:
                search_output_display.value = f"No profile entry discovered for '{query}'."
        
        elif search_mode.value == "Blood Type":
            donors = db.search_by_blood_type(query)
            if donors:
                output_str = f"Discovered {len(donors)} profiles matching Type {query.upper()}:\n\n"
                for d in donors:
                    output_str += f"• {d.get_name()} | Phone: {d.get_contact()}\n"
                search_output_display.value = output_str
            else:
                search_output_display.value = f"No registered entries recorded under type '{query}'."
        page.update()

    search_form_panel = ft.Column(
        [
            ft.Text("Query Search Management Portal", size=18, weight=ft.FontWeight.BOLD),
            search_mode, search_input,
            ft.Row([
                ft.Button(content=ft.Text("Search", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_900, on_click=handle_search_execution)
            ], width=380, alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=15, color=ft.Colors.GREY_300), # FIXED: 'width' property safely removed!
            search_output_display
        ],
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )

    search_layout = ft.Container(
        content=ft.Row([search_form_panel], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.Alignment(0, -1)
    )

    # =========================================================================
    # MAIN APPLICATION STRUCTURE ASSEMBLY (VERIFIED FLET SYSTEM)
    # =========================================================================
    load_live_inventory_records()

    # Define the isolated navigation items
    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="Register"),
            ft.Tab(label="Verify"),
            ft.Tab(label="Inventory"),
            ft.Tab(label="Search"),
        ]
    )

    # Define the separate layout containers matching the order above
    tab_view = ft.TabBarView(
        controls=[
            register_layout,
            eligibility_layout,
            inventory_layout,
            search_layout
        ],
        expand=True
    )

    # Assembly container linking the items via the explicit 'content' wrapper
    app_tabs = ft.Tabs(
        length=4,
        selected_index=0,
        animation_duration=250,
        expand=True,
        content=ft.Column(
            controls=[
                tab_bar,
                tab_view
            ],
            expand=True
        )
    )

    # Append the master UI components directly to the page canvas layout
    page.add(
        ft.AppBar(
            title=ft.Text("Blood Donation System", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_900,
            center_title=True
        ),
        app_tabs
    )

if __name__ == "__main__":
    ft.run(main)