import csv
import os
import time


def show_file_menu():
    """Εμφάνιση μενού επιλογής αρχείου"""
    print("\n" + "=" * 50)
    print("ΕΠΙΛΟΓΗ ΑΡΧΕΙΟΥ ΓΙΑ ΔΙΑΓΡΑΦΗ ΣΤΗΛΩΝ".center(50))
    print("=" * 50)
    print("1. Αρχικό αρχείο (data.csv)")
    print("2. Δειγματοληψία (data_sampled.csv)")
    print("3. BIRCH clustering (data_birched.csv)")
    print("4. Έξοδος")
    print("=" * 50)


def get_file_choice():
    """Λήψη επιλογής αρχείου από τον χρήστη"""
    while True:
        choice = input("Επιλέξτε αρχείο (1-4): ")
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("Μη έγκυρη επιλογή. Παρακαλώ επιλέξτε 1-4.")


def get_input_filename(choice):
    """Αντιστοίχηση επιλογής σε όνομα αρχείου"""
    file_map = {
        "1": "data.csv",
        "2": "new_dataset/data_sampled.csv",
        "3": "new_dataset/data_birched.csv",
    }
    return file_map.get(choice)


def remove_columns(input_file, output_file):
    # Selected via the data exploration notebook instead
    columns_to_drop_nb = [
        "Flow ID",  # ID, υπάρχει η πληροφορία αλλού
        "Timestamp",  # Δεν είναι χρήσιμη για ανάλυση
        "Bwd PSH Flags",  # επειδή είναι πάντα 0
        "Bwd URG Flags",  # επειδή είναι πάντα 0
        "Fwd Bytes/Bulk Avg",  # επειδή είναι πάντα 0
        "Fwd Packet/Bulk Avg",  # επειδή είναι πάντα 0
        "Fwd Bulk Rate Avg",  # επειδή είναι πάντα 0
        "Fwd IAT Total",  # λογω correlation με Flow Duration
        "Subflow Fwd Packets",  # λογω correlation με Total Fwd Packet
        "Subflow Bwd Packets",  # λογω correlation με Total Bwd packets
        "Fwd Act Data Pkts",  # λογω correlation με Total Length of Fwd Packet
        "Fwd Packet Length Min",  # λογω correlation με Fwd Packet Length Max
        "Fwd Packet Length Mean",  # λογω correlation με Fwd Packet Length Max
        "Fwd Packet Length Max",  # λογω correlation με Packet Length Max
        "Packet Length Mean",  # λογω correlation με Fwd Packet Length Max
        "Fwd Segment Size Avg",  # λογω correlation με Fwd Packet Length Max
        "Bwd Packet Length Std",  # λογω correlation με Bwd Packet Length Max
        "Bwd Segment Size Avg",  # λογω correlation με Bwd Packet Length Mean
        "Fwd Packets/s",  # λογω correlation με Flow Packets/s
        "Flow IAT Mean",  # λογω correlation με Flow IAT Max
        "Fwd IAT Mean",  # λογω correlation με Flow IAT Max
        "Fwd IAT Max",  # λογω correlation με Flow IAT Max
        "Idle Mean",  # λογω correlation με Flow IAT Max
        "Flow IAT Max",  # λογω correlation με Idle Max
        "Idle Min",  # λογω correlation με Flow IAT Max
        "Fwd IAT Min",  # λογω correlation με Fwd IAT Mean
        "Bwd IAT Std",  # λογω correlation με Bwd IAT Max
        "ACK Flag Count",  # λογω correlation με Fwd Header Length
        "Packet Length Max",  # λογω correlation με Average Packet Size
        "Packet Length Std",  # λογω correlation με Packet Length Variance
        "PSH Flag Count",  # λογω correlation με ACK Flag Count
        "Bwd Packet/Bulk Avg",  # λογω correlation με Bwd Bytes/Bulk Avg
        "Active Mean",  # λογω correlation με Active Max
        "Active Min",  # λογω correlation με Active Mean
    ]

    columns_to_drop = [
        "Total Length of Fwd Packet",  # λογω correlation με total bwd packet
        "Total Length of Bwd Packet",  # λογω correlation με total fwd packet
        "Fwd Packet Length Min",  # λογω correlation με mean
        "Fwd Packet Length Max",  # λογω correlation με mean
        "Average Packet Size",  # λογω correlation με packet length mean
        "Bwd Packet Length Max",  # λογω correlation με mean
        "Fwd PSH Flags",  # λογω correlation με ack flag
        "Bwd IAT Min",  # λογω correlation με bwd IAT mean
        "Fwd IAT Min",  # λόγω correlation με fwd IAT mean
        "Fwd IAT Total",  # λογω correlation με total fwd packet length
        "Fwd Init Win Bytes",  # λογω correlation με SYN Flag Count
        "Fwd IAT Mean",  # λογω correlation με Flow IAT mean
        "Fwd IAT Std",  # λογω correlation με Flow IAT std
        "Fwd Packet Length Std",  # λογω correlation με flow duration
        "Fwd Packets/s",  # λογω correlation με backward packets
        "Bwd Bytes/Bulk Avg",  # λογω correlation με bwd segment size avg
        "Bwd Packet/Bulk Avg",  # λογω correlation με bwd bytes/bulk avg
        "Fwd Segment Size Avg",  # λογω correlation με packet length mean
        "Subflow Bwd Packets",  # λογω correlation με subflow fwd packets
        "Active Min",  # λογω correlation με active mean
        "Flow IAT Max",  # λογω correlation με fwd IAT max
        "Packet Length Std",  # λογω correlation με packet length max
        "Active Max",  # λογω correlation με active mean
        "Idle Max",  # λογω correlation με idle mean
        "Fwd Header Length",  # λογω correlation με flow duration
        "Bwd Header Length",  # λογω correlation με flow duration
        "Packet Length Max",  # λογω correlation με fwd packet length mean
        "Fwd Act Data Pkts",  # λογω correlation με PSH Flag Count
        "ACK Flag Count",  # λογω correlation με PSH Flag Count
        "Subflow Fwd Bytes",  # λογω correlation με Subflow Fwd Packets
        "Idle Min",  # λογω correlation με idle mean
        "Fwd Packet Length Mean",  # λογω correlation με packet length mean
        "Total Fwd Packet",  # λογω correlation με PSH Flag Count
        "Bwd Segment Size Avg",  # λογω correlation με bwd packet length mean
        "Bwd PSH Flags",  # επειδή είναι πάντα 0
        "Fwd URG Flags",  # επειδή είναι πάντα 0
        "Bwd URG Flags",  # επειδή είναι πάντα 0
        "CWR Flag Count",  # επειδή είναι πάντα 0
        "ECE Flag Count",  # επειδή είναι πάντα 0
        "URG Flag Count",  # επειδή είναι πάντα 0
        "Fwd Packet/Bulk Avg",  # επειδή είναι πάντα 0
        "Fwd Bytes/Bulk Avg",  # επειδή είναι πάντα 0
        "Fwd Bulk Rate Avg",  # επειδή είναι πάντα 0
    ]

    print(
        "Μετράμε το συνολικό αριθμό γραμμών (αυτό μπορεί να πάρει λίγο χρόνο)..."
    )
    with open(input_file, "r") as infile:
        total_rows = sum(1 for _ in infile) - 1  # Αφαιρούμε τη γραμμή κεφαλίδας
    print(f"Βρέθηκαν {total_rows:,} γραμμές προς επεξεργασία")

    # επεξεργαζόμαστε το αρχείο
    processed_rows = 0
    last_percent_reported = -1
    start_time = time.time()

    with open(input_file, "r") as infile, open(
        output_file, "w", newline=""
    ) as outfile:
        reader = csv.DictReader(infile)

        # Βρίσκουμε ποιες στήλες να κρατήσουμε
        fieldnames = [
            col for col in reader.fieldnames if col not in columns_to_drop_nb
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        print("\nΕπεξεργασία γραμμών...")
        for row in reader:
            # Φιλτράρουμε τη γραμμή
            filtered_row = {col: row[col] for col in fieldnames}
            writer.writerow(filtered_row)

            # Ενημέρωση προόδου
            processed_rows += 1
            percent_complete = int((processed_rows / total_rows) * 100)

            # Εκτύπωση μόνο όταν αλλάζει το ποσοστό (για αποφυγή υπερβολικής εξόδου)
            if percent_complete != last_percent_reported:
                if percent_complete % 10 == 0:  # Εκτύπωση κάθε 5%
                    elapsed_time = time.time() - start_time
                    rows_per_second = (
                        processed_rows / elapsed_time if elapsed_time > 0 else 0
                    )
                    remaining_time = (
                        (total_rows - processed_rows) / rows_per_second
                        if rows_per_second > 0
                        else 0
                    )

                    print(
                        f"{percent_complete}% ολοκληρώθηκε | "
                        f"Επεξεργασμένες: {processed_rows:,}/{total_rows:,} | "
                        f"Ταχύτητα: {rows_per_second:,.0f} γραμμές/δευτ | "
                        f"Εκτιμώμενος χρόνος: {remaining_time/60:.1f} λεπτά"
                    )
                    last_percent_reported = percent_complete

    # Τελική κατάσταση
    elapsed_time = time.time() - start_time
    print(
        f"\nΗ επεξεργασία ολοκληρώθηκε! Επεξεργάστηκαν {processed_rows:,} γραμμές σε {elapsed_time/60:.2f} λεπτά"
    )
    print(f"Μέση ταχύτητα: {processed_rows/elapsed_time:,.0f} γραμμές/δευτ")
    print(
        f"Αφαιρέθηκαν {len(columns_to_drop_nb)} στήλες, διατηρήθηκαν {len(fieldnames)} στήλες"
    )


def main():
    """Κύρια λειτουργία του προγράμματος"""
    print("\n" + "=" * 50)
    print("ΕΡΓΑΛΕΙΟ ΔΙΑΓΡΑΦΗΣ ΣΤΗΛΩΝ".center(50))
    print("=" * 50)

    while True:
        show_file_menu()
        choice = get_file_choice()

        if choice == "4":
            print("\nΤερματισμός προγράμματος...")
            break

        input_file = get_input_filename(choice)
        if not os.path.exists(input_file):
            print(f"\nΣφάλμα: Το αρχείο '{input_file}' δεν βρέθηκε!")
            continue

        output_file = f"data_cut.csv"

        print(f"\nΕπεξεργασία αρχείου: {input_file}")
        print(
            "Προσοχή: Αυτή η διαδικασία μπορεί να πάρει λίγο χρόνο για μεγάλα αρχεία..."
        )

        remove_columns(input_file, output_file)

        cont = input("\nΘέλετε να επεξεργαστείτε άλλο αρχείο; (y/n): ").lower()
        if cont != "y":
            break


if __name__ == "__main__":
    main()
