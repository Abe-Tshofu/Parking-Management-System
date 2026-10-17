from __future__ import annotations

from service import ParkingService


def print_mall_list(service: ParkingService) -> None:
    print("\nMalls and pricing rules:")
    for mall in service.list_malls():
        if mall.pricing_type == "flat":
            pricing_text = f"Flat rate: R{mall.rate:.2f} per visit"
        elif mall.pricing_type == "hourly":
            pricing_text = f"R{mall.rate:.2f} per hour or part thereof"
        else:
            pricing_text = f"R{mall.rate:.2f} per hour or part thereof, capped at R60.00 per day"
        print(f"- {mall.name}: {pricing_text} | Capacity: {mall.capacity}")


def customer_menu(service: ParkingService, username: str) -> None:
    while True:
        print("\nCustomer menu")
        print("1. View malls")
        print("2. Entry vehicle")
        print("3. Exit vehicle")
        print("4. View outstanding fees")
        print("5. Record payment")
        print("6. View payment history")
        print("7. Logout")

        choice = input("Select an option: ").strip()

        if choice == "1":
            print_mall_list(service)
        elif choice == "2":
            print_mall_list(service)
            mall_name = input("Select mall name: ").strip()
            vehicle_reg = input("Enter vehicle registration: ").strip()
            print(service.enter_vehicle(username, mall_name, vehicle_reg))
        elif choice == "3":
            vehicle_reg = input("Enter vehicle registration to exit: ").strip()
            print(service.exit_vehicle(username, vehicle_reg))
        elif choice == "4":
            outstanding = service.outstanding_fees(username)
            if not outstanding:
                print("No outstanding fees found.")
            else:
                print("Outstanding fees:")
                for record in outstanding:
                    print(f"- {record.vehicle_registration} | {record.mall_name} | Due: R{record.fee_amount - record.paid_amount:.2f}")
        elif choice == "5":
            vehicle_reg = input("Enter vehicle registration: ").strip()
            amount = input("Enter payment amount: ").strip()
            try:
                print(service.record_payment(username, vehicle_reg, float(amount)))
            except ValueError:
                print("Payment amount must be a valid number.")
        elif choice == "6":
            payments = service.payment_history(username)
            if not payments:
                print("No payment history found.")
            else:
                print("Payment history:")
                for payment in payments:
                    print(f"- {payment.payment_time} | {payment.vehicle_registration} | {payment.mall_name} | R{payment.amount:.2f}")
        elif choice == "7":
            print("Logged out.")
            return
        else:
            print("Invalid option. Please try again.")


def admin_menu(service: ParkingService) -> None:
    while True:
        print("\nAdmin menu")
        print("1. View currently parked vehicles")
        print("2. View available spaces")
        print("3. View daily activity")
        print("4. Logout")

        choice = input("Select an option: ").strip()
        summary = service.get_admin_summary()

        if choice == "1":
            if not summary["active_records"]:
                print("No vehicles are currently parked.")
            else:
                print("Currently parked vehicles:")
                for record in summary["active_records"]:
                    print(f"- {record.vehicle_registration} | {record.mall_name} | Entry: {record.entry_time}")
        elif choice == "2":
            print("Available parking spaces:")
            for mall_name, spaces in summary["available_spaces"].items():
                print(f"- {mall_name}: {spaces} spaces available")
        elif choice == "3":
            print(f"Completed parking records: {summary['total_completed_records']}")
            print(f"Daily income: R{summary['daily_income']:.2f}")
        elif choice == "4":
            print("Logged out.")
            return
        else:
            print("Invalid option. Please try again.")


def owner_menu(service: ParkingService) -> None:
    while True:
        print("\nOwner menu")
        print("1. View mall performance report")
        print("2. Logout")

        choice = input("Select an option: ").strip()

        if choice == "1":
            report = service.owner_report()
            print("Mall performance report")
            for mall_name, values in report.items():
                print(
                    f"- {mall_name}: Activity={values['activity_count']} | "
                    f"Revenue=R{values['total_revenue']:.2f} | "
                    f"Avg Duration={values['average_duration_minutes']:.2f} minutes"
                )
        elif choice == "2":
            print("Logged out.")
            return
        else:
            print("Invalid option. Please try again.")


def main() -> None:
    service = ParkingService()

    while True:
        print("\nKZN Smart Mall Parking Management System")
        print("1. Register customer")
        print("2. Customer login")
        print("3. Admin login")
        print("4. Owner login")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            full_name = input("Enter full name: ").strip()
            print(service.register_customer(username, password, full_name))
        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            user = service.login(username, password)
            if user and user.role == "customer":
                customer_menu(service, user.username)
            else:
                print("Invalid customer login details.")
        elif choice == "3":
            username = input("Enter admin username: ").strip()
            password = input("Enter admin password: ").strip()
            user = service.login(username, password)
            if user and user.role == "admin":
                admin_menu(service)
            else:
                print("Invalid admin login details.")
        elif choice == "4":
            username = input("Enter owner username: ").strip()
            password = input("Enter owner password: ").strip()
            user = service.login(username, password)
            if user and user.role == "owner":
                owner_menu(service)
            else:
                print("Invalid owner login details.")
        elif choice == "5":
            print("Thank you for using KZN Smart Mall Parking System.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
