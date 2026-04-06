package Object_Oriented_Programming;

import java.util.*;
import java.io.*;


// =========================================
// ABSTRACT INTERFACE (ABSTRACTION)
// =========================================

// ABSTRACTION: The interface hides HOW searching works.
// Only the method names are exposed—implementation happens elsewhere.
// This is a key example of ABSTRACTION, as it defines a contract without specifying details.
interface Searchable {
    void searchByName(String name);
    void searchByBloodType(String type);
}


// =========================================
// PARENT CLASS (INHERITANCE + ENCAPSULATION)
// =========================================
class Person {

    // ENCAPSULATION: Fields are private and accessed only through getters.
    // This demonstrates ENCAPSULATION by protecting data and controlling access.
    private String name;
    private int age;
    private String contact;

    // Constructor initializes encapsulated data.
    public Person(String name, int age, String contact) {
        this.name = name;
        this.age = age;
        this.contact = contact;
    }

    // Method to display common info for all persons.
    public void displayInfo() {
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Contact: " + contact);
    }

    // ENCAPSULATION: Controlled access to private fields via getters.
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getContact() { return contact; }
}


// =========================================
// CHILD CLASS (INHERITANCE + POLYMORPHISM)
// =========================================

// INHERITANCE: Donor inherits fields/methods from Person.
// This shows INHERITANCE, allowing Donor to reuse Person's attributes and methods.
// POLYMORPHISM: Donor overrides displayInfo() to add more info.
// This demonstrates POLYMORPHISM through method overriding.
class Donor extends Person {

    // Additional attributes only a Donor has.
    private String bloodType;
    private double weight;

    // Inherits name, age, and contact from Person via super().
    // INHERITANCE: Using super() to call parent constructor.
    public Donor(String name, int age, String bloodType, double weight, String contact) {
        super(name, age, contact);
        this.bloodType = bloodType;
        this.weight = weight;
    }

    // POLYMORPHISM: Overriding the displayInfo() of the parent class.
    // This is POLYMORPHISM, as the method behaves differently for Donor objects.
    @Override
    public void displayInfo() {
        // Calls parent method → polymorphic behavior.
        super.displayInfo();
        System.out.println("Blood Type: " + bloodType);
        System.out.println("Weight: " + weight);
    }

    // Encapsulated getter for extra fields
    // ENCAPSULATION: Providing controlled access to private fields.
    public String getBloodType() { return bloodType; }
    public double getWeight() { return weight; }
}


// =========================================
// DONOR DATABASE
// =========================================
class DonorArray {

    // ENCAPSULATION: donor list is private and only modifiable through methods.
    // This ensures ENCAPSULATION by hiding the list and controlling modifications.
    private ArrayList<Donor> donors = new ArrayList<>();

    public void addDonor(Donor d) {
        donors.add(d);
    }

    // Returns list for searching
    public ArrayList<Donor> getList() {
        return donors;
    }
}


// =========================================
// SEARCH MODULE (POLYMORPHISM)
// =========================================

// POLYMORPHISM: Implements Searchable interface → must override methods.
// This shows POLYMORPHISM through interface implementation and method overriding.
class DonorSearch implements Searchable {

    // Composition: Uses donor list to search.
    private ArrayList<Donor> donors;

    public DonorSearch(ArrayList<Donor> donors) {
        this.donors = donors;
    }

    // POLYMORPHISM: Implementing interface-defined methods.
    // Overriding methods from Searchable interface demonstrates POLYMORPHISM.
    @Override
    public void searchByName(String name) {
        for (Donor d : donors) {
            if (d.getName().equalsIgnoreCase(name)) {
                d.displayInfo(); // Polymorphic call (overridden method)
                return;
            }
        }
        System.out.println("Donor not found.");
    }

    @Override
    public void searchByBloodType(String type) {
        boolean found = false;
        for (Donor d : donors) {
            if (d.getBloodType().equalsIgnoreCase(type)) {
                d.displayInfo(); // Polymorphic call
                found = true;
            }
        }
        if (!found) {
            System.out.println("No donors match that blood type.");
        }
    }
}


// =========================================
// BLOOD INVENTORY SYSTEM
// =========================================
class BloodInventory {

    // ENCAPSULATION: inventory hidden and modified only through class methods.
    // This demonstrates ENCAPSULATION by keeping the map private and using methods for access.
    private HashMap<String, Integer> inventory = new HashMap<>();

    public BloodInventory() {
        inventory.put("A+",0); inventory.put("A-",0);
        inventory.put("B+",0); inventory.put("B-",0);
        inventory.put("O+",0); inventory.put("O-",0);
        inventory.put("AB+",0); inventory.put("AB-",0);
    }

    public void addBlood(String type, int units) {
        inventory.put(type, inventory.getOrDefault(type, 0) + units);
        System.out.println(units + " units added.");
    }

    public void viewInventory() {
        System.out.println("\n=== Available Blood Units ===");
        for (String type : inventory.keySet()) {
            System.out.println(type + ": " + inventory.get(type));
        }
    }
}


// =========================================
// MAIN SYSTEM (USES POLYMORPHISM FOR SEARCH)
// =========================================
public class BloodDonationSystem {

    private static Scanner sc = new Scanner(System.in);
    private static BloodInventory inventory = new BloodInventory();
    private static DonorArray donorDB = new DonorArray();

    public static void main(String[] args) {

        int choice;

        do {
            System.out.println("\n=== BLOOD DONATION SYSTEM ===");
            System.out.println("1. Register Donor");
            System.out.println("2. Check Eligibility");
            System.out.println("3. Blood Inventory");
            System.out.println("4. Search Donor");
            System.out.println("5. Exit");
            System.out.print("Enter choice: ");

            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1: registerDonor(); break;
                case 2: eligibilityChecker(); break;
                case 3: inventoryMenu(); break;
                case 4: searchDonor(); break;
                case 5: System.out.println("Thank you for using the system!"); break;
                default: System.out.println("Invalid choice.");
            }

        } while (choice != 5);
    }


    // ___________________________
    // REGISTER DONOR
    private static void registerDonor() {

        System.out.println("\n== Donor Registration ==");

        System.out.print("Name: ");
        String name = sc.nextLine();

        System.out.print("Age: ");
        int age = sc.nextInt();

        System.out.print("Weight: ");
        double weight = sc.nextDouble();
        sc.nextLine();

        System.out.print("Blood Type (O, A, B, AB): ");
        String blood = sc.nextLine().toUpperCase();

        System.out.print("Rhesus (+ or -): ");
        String rh = sc.nextLine();

        System.out.print("Contact: ");
        String contact = sc.nextLine();

        Donor donor = new Donor(name, age, blood + rh, weight, contact);
        donorDB.addDonor(donor);

        System.out.println("Donor registered successfully!");
    }


    // ___________________________
    // ELIGIBILITY CHECKER
    private static void eligibilityChecker() {
        System.out.println("\n== Eligibility Checker ==");

        System.out.print("Age: ");
        int age = sc.nextInt();

        System.out.print("Weight: ");
        double weight = sc.nextDouble();

        System.out.print("Months since last donation: ");
        int months = sc.nextInt();
        sc.nextLine();

        System.out.print("Any illness? (yes/no): ");
        String ill = sc.nextLine();

        boolean eligible = (age >= 18 && age <= 65) &&
                           (weight >= 50) &&
                           (months >= 3) &&
                           (ill.equalsIgnoreCase("no"));

        if (eligible)
            System.out.println("You are eligible to donate!");
        else
            System.out.println("You are NOT eligible to donate.");
    }


    // ___________________________
    // INVENTORY MENU
    private static void inventoryMenu() {
        int choice;

        do {
            System.out.println("\n== Blood Inventory ==");
            System.out.println("1. Add Blood Units");
            System.out.println("2. View Inventory");
            System.out.println("3. Back");
            System.out.print("Enter: ");

            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    System.out.print("Blood Type: ");
                    String type = sc.nextLine().toUpperCase();

                    System.out.print("Units: ");
                    int units = sc.nextInt();

                    inventory.addBlood(type, units);
                    break;

                case 2:
                    inventory.viewInventory();
                    break;
            }
        } while (choice != 3);
    }


    // ___________________________
    // SEARCH DONOR
    private static void searchDonor() {
        System.out.println("\n== Search Donor ==");
        System.out.println("1. By Name");
        System.out.println("2. By Blood Type");
        System.out.print("Enter: ");

        int opt = sc.nextInt();
        sc.nextLine();

        // POLYMORPHISM: Searchable reference pointing to DonorSearch object
        // This demonstrates POLYMORPHISM, as Searchable can refer to any implementing class.
        Searchable search = new DonorSearch(donorDB.getList());

        if (opt == 1) {
            System.out.print("Enter name: ");
            search.searchByName(sc.nextLine());
        }
        else if (opt == 2) {
            System.out.print("Enter blood type: ");
            search.searchByBloodType(sc.nextLine());
        }
    }
}
