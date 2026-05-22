import flet as ft
from BloodDonationSystem import BloodDonationDatabase, Donor 

def main(page: ft.Page):
    page.window_width = 390
    page.window_height = 844
    page.window_resizable = False
    page.title = "Blood Bank App"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Connection layout matching your XAMPP settings
    db = BloodDonationDatabase(
        host="localhost",
        user="root",
        password="", 
        database="blood_donation_system_database"
    )

    # Clean UI structures
    search_input = ft.TextField(
        label="Search Query", 
        hint_text="e.g., John Doe or O+",
        border_radius=10,
    )
    
    search_mode = ft.Dropdown(
        label="Search By",
        value="Name",
        options=[
            ft.dropdown.Option("Name"),
            ft.dropdown.Option("Blood Type"),
        ],
        border_radius=10
    )
    
    result_text = ft.Text(size=15, color=ft.Colors.WHITE)

    def on_search_click(e):
        query_value = search_input.value.strip()
        
        if not query_value:
            result_text.value = "Please enter a search value!"
            result_text.color = ft.Colors.ORANGE_400
            page.update()
            return

        if search_mode.value == "Name":
            donor = db.search_by_name(query_value)
            if donor:
                result_text.value = (
                    f"Donor Found!\n\n"
                    f"Name: {donor.get_name()}\n"
                    f"Age: {donor.get_age()}\n"
                    f"Contact: {donor.get_contact()}\n"
                    f"Blood Type: {donor.get_blood_type()}\n"
                    f"Weight: {donor.get_weight()} kg"
                )
                result_text.color = ft.Colors.GREEN_ACCENT
            else:
                result_text.value = f"No donor found with the name '{query_value}'"
                result_text.color = ft.Colors.RED_ACCENT

        elif search_mode.value == "Blood Type":
            donors_list = db.search_by_blood_type(query_value)
            if donors_list:
                output = f"Found {len(donors_list)} matching donors:\n\n"
                for d in donors_list:
                    output += f"• {d.get_name()} | Blood Type: {d.get_blood_type()} | Contact: {d.get_contact()}\n"
                result_text.value = output
                result_text.color = ft.Colors.GREEN_ACCENT
            else:
                result_text.value = f"No donors found with blood type '{query_value}'"
                result_text.color = ft.Colors.RED_ACCENT
                
        page.update()

    # Fixed for newest Flet spec: Using ft.Button + content property
    search_button = ft.Button(
        content=ft.Text("Find Donors", color=ft.Colors.WHITE),
        on_click=on_search_click,
        bgcolor=ft.Colors.RED_ACCENT_400,
        height=50
    )

    page.add(
        ft.AppBar(
            title=ft.Text("Blood Donation System", weight=ft.FontWeight.BOLD), 
            bgcolor=ft.Colors.RED_900,
            center_title=True
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Database Lookup Engine", size=18, weight=ft.FontWeight.W_500),
                search_mode,
                search_input,
                ft.Row([search_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=30, color=ft.Colors.GREY_800),
                ft.Column([result_text], scroll=ft.ScrollMode.AUTO, expand=True)
            ], spacing=15),
            padding=20,
            expand=True
        )
    )

if __name__ == "__main__":
    # Fixed for newest Flet spec: Using run() instead of app()
    ft.app(target=main)