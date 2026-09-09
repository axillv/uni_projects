import enum
import os
import random
import time
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from sklearn.cluster import Birch, KMeans
from sklearn.preprocessing import StandardScaler

# Απενεργοποίηση προειδοποιήσεων
warnings.filterwarnings("ignore")
# Δημιουργία φακέλου για αποθήκευση αν δεν υπάρχει
os.makedirs("new_dataset", exist_ok=True)


def show_menu():
    """Εμφάνιση μενού επιλογών"""
    print("\n" + "=" * 50)
    print("ΚΥΡΙΟ ΜΕΝΟΥ".center(50))
    print("=" * 50)
    print("1. Δειγματοληψία (Sampling)")
    print("2. Συσταδοποίηση με αλγόριθμο BIRCH")
    print("3. Συσταδοποίηση με αλγόριθμο K-Means")
    print("4. Έξοδος")
    print("=" * 50)


def get_input_file():
    """Επιλογή αρχείου εισόδου"""
    print("\nΕπιλέξτε αρχείο εισόδου:")
    print("1. Αρχικό αρχείο (data.csv)")
    print("2. Αρχικό αρχείο με αφαίρεση στηλών (data_cut.csv)")
    print("3. Αποτέλεσμα δειγματοληψίας (data_sampled.csv)")
    print("4. Κανονικοποιημένα Benign (new_dataset/benign_normalized.csv)")
    print(
        "5. Κανονικοποιημένα Malicious (new_dataset/malicious_normalized.csv)"
    )
    choice = input("Επιλογή (1/2/3/4/5): ")
    match choice:
        case "1":
            return "data.csv"
        case "2":
            return "data_cut.csv"
        case "3":
            return "data_sampled.csv"
        case "4":
            return os.path.join("new_dataset", "benign_normalized.csv")
        case "5":
            return os.path.join("new_dataset", "malicious_normalized.csv")
        case _:
            print("Μη έγκυρη επιλογή. Επιλογή προεπιλογής: data.csv")
            return "data.csv"


def get_n_rows(choice):
    """Εισαγωγή αριθμού γραμμών από τον χρήστη"""
    while True:
        try:
            if choice:
                # Αριθμός γραμμών για δειγματοληψία
                n_rows = input(
                    "\nΕισάγετε τον αριθμό γραμμών που θέλετε στο δείγμα: "
                )
                return int(n_rows)
            else:
                # Αριθμός γραμμών για BIRCH
                n_rows = input(
                    "\nΕισαγάγετε αριθμό γραμμών (-1 για όλο το dataset): "
                )
                return int(n_rows)
        except ValueError:
            print("Παρακαλώ εισάγετε έγκυρο ακέραιο αριθμό.")


def perform_sampling(n_rows):
    """Εκτέλεση δειγματοληψίας"""
    try:
        # Υπολογισμός μεγέθους δείγματος
        sample_size = n_rows
        # Επιλογή αρχείου εισόδου
        input_file = get_input_file()

        # Υπολογισμός συνολικών γραμμών στο αρχείο
        with open(input_file, "r") as f:
            header = next(f)
            total_rows = sum(1 for _ in f)

        sample_rows_indices = random.sample(range(total_rows), sample_size)
        sample_rows_indices.sort()
        selected_rows = []

        # Επιλογή γραμμών με βάση την λίστα
        with open(input_file, "r") as f:
            row_to_sample_index = 0
            row_to_sample = sample_rows_indices[row_to_sample_index]

            for i, line in enumerate(f):
                if i == row_to_sample:
                    selected_rows.append(line.strip())
                    row_to_sample_index += 1
                    if row_to_sample_index == len(sample_rows_indices):
                        break  # check if sampling is finished

                    row_to_sample = sample_rows_indices[row_to_sample_index]

        # Αποθήκευση αποτελεσμάτων σε νέο αρχείο
        output_file = os.path.join("new_dataset", "data_sampled.csv")
        if os.path.exists(output_file):
            os.remove(output_file)

        with open(output_file, "w") as f:
            f.write(header + "\n")
            for row in selected_rows:
                f.write(row + "\n")

        data = pd.read_csv(output_file)

        # Εμφάνιση αποτελεσμάτων στον χρήστη
        print("\n" + "=" * 50)
        print("ΔΕΙΓΜΑΤΟΛΗΨΙΑ ΟΛΟΚΛΗΡΩΘΗΚΕ".center(50))
        print("=" * 50)
        print(f"Τυχαίο δείγμα {len(data)} γραμμών από σύνολο {total_rows}")
        print(f"Το δείγμα αποθηκεύτηκε στο: '{output_file}'")

    except Exception as e:
        # Διαχείριση σφαλμάτων
        print(f"\nΣφάλμα κατά τη δειγματοληψία: {e}")
        print("Αναλυτικό σφάλμα:", str(e))
        import traceback

        traceback.print_exc()


def _process_data_chunks(input_file, n_rows, process_fn=None):
    """Κοινή λογική επεξεργασίας τμημάτων δεδομένων για BIRCH και K-Means"""
    CHUNKSIZE = 20000  # Μέγεθος τμημάτων για ανάγνωση
    OUTPUT_DIR = "new_dataset"
    scaler = StandardScaler()  # Κανονικοποίηση δεδομένων

    try:
        # Δημιουργία φακέλου για αποθήκευση
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except Exception as e:
        print(f"Σφάλμα δημιουργίας φακέλου: {e}")
        return None, None, None

    total_rows = 0
    processed_chunks = []  # Αποθήκευση επεξεργασμένων δεδομένων
    original_chunks = []  # Αποθήκευση αρχικών δεδομένων
    start_time = time.time()

    try:
        # Έλεγχος αν θα επεξεργαστούμε όλες τις γραμμές
        process_all = n_rows == -1
        rows_to_process = (
            "όλες τις γραμμές"
            if process_all
            else f"τις πρώτες {n_rows:,} γραμμές"
        )
        print(
            f"\nΕπεξεργασία {rows_to_process} από το αρχείο '{input_file}'..."
        )

        # Ανάγνωση δεδομένων σε τμήματα
        for i, chunk in enumerate(
            pd.read_csv(
                input_file,
                chunksize=CHUNKSIZE,
                nrows=None if process_all else n_rows,
            )
        ):
            original_chunks.append(chunk.copy())
            numeric_data = chunk.select_dtypes(include=["number"]).fillna(
                0
            )  # Επιλογή αριθμητικών δεδομένων
            numeric_data_scaled = pd.DataFrame(
                scaler.fit_transform(numeric_data), columns=numeric_data.columns
            )
            processed_chunks.append(numeric_data_scaled.copy())
            total_rows += len(numeric_data_scaled)

            # Σε περίπτωση birch, χρειάζεται να γίνει partial_fit
            if process_fn:
                process_fn(numeric_data_scaled)

            if (i + 1) % 10 == 0:
                print(f"Επεξεργάστηκαν {total_rows:,} γραμμές...")

            if not process_all and total_rows >= n_rows:
                break

        # Συγκέντρωση όλων των δεδομένων
        print("\nΣυγκέντρωση αποτελεσμάτων για τελική Συσταδοποίηση...")

        full_original_data = pd.concat(original_chunks)
        if not process_all:
            full_original_data = full_original_data.head(n_rows)

        full_processed_data = pd.concat(processed_chunks)
        if not process_all:
            full_processed_data = full_processed_data.head(n_rows)

        return full_original_data, full_processed_data, start_time

    except Exception as e:
        # Διαχείριση σφαλμάτων
        print(f"\nΚρίσιμο σφάλμα κατά την επεξεργασία: {e}")
        print("Αναλυτικό σφάλμα:", str(e))
        import traceback

        traceback.print_exc()
        return None, None, None


def perform_birch(input_file, n_rows):
    """Εκτέλεση clustering με BIRCH"""
    # TODO: Calculate appropriate settings
    try:
        # Αρχικοποίηση του μοντέλου BIRCH
        birch = Birch(
            threshold=2,
            branching_factor=200,
            n_clusters=13000,
            compute_labels=True,
        )

        def birch_partial_fit(data):
            birch.partial_fit(data)

        # Επεξεργασία δεδομένων
        full_original_data, full_processed_data, start_time = (
            _process_data_chunks(input_file, n_rows, birch_partial_fit)
        )

        if full_original_data is None:
            return

        # Υπολογισμός συστάδων
        print("Υπολογισμός τελικών συστάδων...")
        labels = birch.predict(full_processed_data)
        full_original_data["cluster"] = labels

        # Αποθήκευση αποτελεσμάτων
        output_path = os.path.join("new_dataset", "data_birched.csv")
        full_original_data.to_csv(output_path, index=False)

        # Αποθήκευση πληροφοριών clustering
        info_path = os.path.join("new_dataset", "birch_info.txt")
        with open(info_path, "w", encoding="utf-8") as f:
            f.write(f"Συνολικές γραμμές: {len(full_original_data):,}\n")
            f.write(f"Αριθμός συστάδων: {len(np.unique(labels))}\n")
            f.write(
                f"Χρόνος εκτέλεσης: {time.time()-start_time:.2f} δευτερόλεπτα\n"
            )

        # Εμφάνιση αποτελεσμάτων στον χρήστη
        print("\n" + "=" * 50)
        print("BIRCH CLUSTERING ΟΛΟΚΛΗΡΩΘΗΚΕ".center(50))
        print("=" * 50)
        print(f"Αποτελέσματα αποθηκεύτηκαν στο: {output_path}")
        print(f"Αριθμός συστάδων: {len(np.unique(labels))}")
        print(f"Συνολικός χρόνος: {time.time()-start_time:.2f} δευτερόλεπτα")

    except Exception as e:
        # Διαχείριση σφαλμάτων
        print(f"\nΚρίσιμο σφάλμα κατά την επεξεργασία: {e}")
        print("Αναλυτικό σφάλμα:", str(e))
        import traceback

        traceback.print_exc()


def perform_kmeans(input_file, n_rows):
    """Εκτέλεση clustering με K-Means"""
    N_CLUSTERS = 13000  # Αριθμός συστάδων (μπορεί να αλλαχτεί)

    try:
        # Επεξεργασία δεδομένων
        full_original_data, full_processed_data, start_time = (
            _process_data_chunks(input_file, n_rows)
        )

        if full_original_data is None:
            return

        # Εφαρμογή K-Means
        print("Εκτέλεση K-Means clustering...")

        # Χρησιμοποιούμε τον αλγόριθμο K-Means++ για καλύτερη αρχικοποίηση
        kmeans = KMeans(
            n_clusters=N_CLUSTERS, init="k-means++", n_init=10, random_state=42
        )
        labels = kmeans.fit_predict(full_processed_data)

        full_original_data["cluster"] = labels

        # Αποθήκευση αποτελεσμάτων
        output_path = os.path.join("new_dataset", "data_kmeaned.csv")
        full_original_data.to_csv(output_path, index=False)

        # Αποθήκευση πληροφοριών clustering
        info_path = os.path.join("new_dataset", "kmeans_info.txt")
        with open(info_path, "w", encoding="utf-8") as f:
            f.write(f"Συνολικές γραμμές: {len(full_original_data):,}\n")
            f.write(f"Αριθμός συστάδων: {N_CLUSTERS}\n")
            f.write(
                f"Χρόνος εκτέλεσης: {time.time()-start_time:.2f} δευτερόλεπτα\n"
            )
            f.write(f"Αρχικοποίηση: K-Means++\n")
            f.write(f"Επαναλήψεις: {kmeans.n_iter_}\n")

        # Εμφάνιση αποτελεσμάτων στον χρήστη
        print("\n" + "=" * 50)
        print("K-MEANS CLUSTERING ΟΛΟΚΛΗΡΩΘΗΚΕ".center(50))
        print("=" * 50)
        print(f"Αποτελέσματα αποθηκεύτηκαν στο: {output_path}")
        print(f"Αριθμός συστάδων: {N_CLUSTERS}")
        print(f"Συνολικός χρόνος: {time.time()-start_time:.2f} δευτερόλεπτα")

    except Exception as e:
        # Διαχείριση σφαλμάτων
        print(f"\nΚρίσιμο σφάλμα κατά την επεξεργασία: {e}")
        print("Αναλυτικό σφάλμα:", str(e))
        import traceback

        traceback.print_exc()


def main():
    """Κύρια λειτουργία του προγράμματος"""
    while True:
        show_menu()
        choice = input("Επιλέξτε ενέργεια (1-3): ")

        if choice == "1":
            # Δειγματοληψία
            n_rows = get_n_rows(True)
            print("\nΕκτέλεση δειγματοληψίας...")
            perform_sampling(n_rows)

        elif choice == "2":
            # Συσταδοποίηση BIRCH
            input_file = get_input_file()
            n_rows = get_n_rows(False)
            perform_birch(input_file, n_rows)

        elif choice == "3":
            # Συσταδοποίηση K-Means
            input_file = get_input_file()
            n_rows = get_n_rows(False)
            perform_kmeans(input_file, n_rows)

        elif choice == "4":
            # Έξοδος από το πρόγραμμα
            print("\nΤερματισμός προγράμματος...")
            break

        else:
            # Μη έγκυρη επιλογή
            print("\nΜη έγκυρη επιλογή. Παρακαλώ επιλέξτε 1, 2 ή 3.")


if __name__ == "__main__":
    main()
