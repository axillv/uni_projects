import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import ScalarFormatter

# Ρυθμίσεις για την εμφάνιση των δεδομένων
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

warnings.filterwarnings("ignore")


def show_menu():
    """#1.1 Εμφάνιση μενού επιλογής αρχείου"""
    print("\n" + "=" * 50)
    print("ΕΠΙΛΟΓΗ ΑΡΧΕΙΟΥ ΑΝΑΛΥΣΗΣ".center(50))
    print("=" * 50)
    print("1. Αρχικό αρχείο (data.csv)")
    print("2. Αρχικό αρχείο με αφαίρεση στηλών (data_cut.csv)")
    print("3. Δειγματοληψία (data_sampled.csv)")
    print("4. BIRCH clustering (data_birched.csv)")
    print("5. K-MEANS clustering (data_kmeaned.csv)")
    print("6. Έξοδος")
    print("=" * 50)


def load_data(choice, n_rows):
    """#1.2 Φόρτωση δεδομένων βάσει επιλογής"""
    file_map = {
        "1": "data.csv",
        "2": "data_cut.csv",
        "3": "new_dataset/data_sampled.csv",
        "4": "new_dataset/data_birched.csv",
        "5": "new_dataset/data_kmeaned.csv",
    }

    file_path = file_map.get(choice)
    if not file_path:
        return None

    try:
        data = pd.read_csv(file_path, nrows=n_rows)
        print(f"\nΔεδομένα φορτώθηκαν επιτυχώς από: {file_path}")
        return data
    except Exception as e:
        print(f"\nΣφάλμα κατά τη φόρτωση: {e}")
        return None


def get_n_rows():
    """Εισαγωγή αριθμού γραμμών από τον χρήστη"""
    while True:
        try:
            # Αριθμός γραμμών για BIRCH
            n_rows = input(
                "\nΕισαγάγετε αριθμό γραμμών που θέλετε να αναλύσετε (καλύτερα μέχρι 500.000): "
            )
            return int(n_rows)
        except ValueError:
            print("Παρακαλώ εισάγετε έγκυρο ακέραιο αριθμό.")


def analyze_columns(df):
    """#1.3 Ανάλυση στηλών"""
    print("\n--- ΠΛΗΡΟΦΟΡΙΕΣ ΣΤΗΛΩΝ ---")
    print("\nΒασικές πληροφορίες:")
    print(df.info())


def calculate_statistics(df):
    """#1.4 Υπολογισμός στατιστικών"""
    print("\n--- ΣΤΑΤΙΣΤΙΚΑ ΜΕΓΕΘΗ ---")
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    print("\nΑριθμητικές στήλες - Βασικά στατιστικά:")
    print(df[numeric_cols].describe().transpose())

    categorical_cols = df.select_dtypes(include=["object"]).columns
    if len(categorical_cols) > 0:
        print("\nΚατηγορηματικές στήλες - Σύνοψη:")
        for col in categorical_cols:
            print(f"\nΣτήλη: {col}")
            print(df[col].value_counts(normalize=True).head(10))

    if "Flow Duration" in df.columns:
        df["Flow Duration Seconds"] = df["Flow Duration"] / 1e6
        print("\nΣτατιστικά Διάρκειας Ροής (σε δευτερόλεπτα):")
        print(df["Flow Duration Seconds"].describe())

    if "Total Fwd Packet" in df.columns:
        print("\nΣτατιστικά Πακέτων:")
        print(df[["Total Fwd Packet", "Total Bwd packets"]].describe())


def create_visualizations(df):
    """#1.5 Δημιουργία γραφικών"""
    print("\n--- ΔΗΜΙΟΥΡΓΙΑ ΓΡΑΦΙΚΩΝ ---")

    # Create directory if it doesn't exist
    os.makedirs("stat_pics", exist_ok=True)

    # Ρυθμίσεις γραφικών
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    plt.rcParams["figure.figsize"] = (10, 6)

    # 1. Κατανομές βασικών μετρικών
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    for col in numeric_cols[:10]:
        try:
            plt.figure()
            if df[col].nunique() > 20:
                # Handle cases where log might fail (negative values)
                if (df[col] < 0).any():
                    sns.histplot(df[col], kde=True)
                    plt.title(f"Κατανομή της {col}")
                else:
                    sns.histplot(np.log1p(df[col]), kde=True)
                    plt.title(f"Κατανομή της {col} (Log Scale)")
                    plt.xlabel(f"log({col})")
            else:
                sns.histplot(df[col], kde=True, bins=20)
                plt.title(f"Κατανομή της {col}")
            plt.tight_layout()

            # Sanitize filename by replacing problematic characters
            safe_colname = col.replace("/", "_").replace("\\", "_")[:20]
            plt.savefig(
                os.path.join("stat_pics", f"distribution_{safe_colname}.png"),
                dpi=300,
            )
            plt.close()
        except Exception as e:
            print(
                f"Σφάλμα κατά τη δημιουργία γραφικού για τη στήλη {col}: {str(e)}"
            )
            plt.close("all")

    # Διαγραφή συγκεκριμένων αρχείων
    files_to_delete = [
        "distribution_Dst Port.png",
        "distribution_Protocol.png",
        "distribution_Src Port.png",
        "distribution_Flow Duration.png",
    ]
    for file in files_to_delete:
        file_path = os.path.join("stat_pics", file)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Το αρχείο {file_path} διαγράφηκε επιτυχώς.")
        else:
            print(f"Το αρχείο {file_path} δεν βρέθηκε.")

    # 2. Ανάλυση Ports και Protocols - with existence checks
    if all(col in df.columns for col in ["Dst Port", "Label"]):
        try:
            plt.figure(figsize=(12, 6))
            top_ports = df["Dst Port"].value_counts().nlargest(10).index
            sns.countplot(
                data=df[df["Dst Port"].isin(top_ports)],
                x="Dst Port",
                hue="Label",
            )
            plt.yscale("log")
            plt.title("Συχνότητα Ports Προορισμού (Top 10)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join("stat_pics", "top_ports.png"), dpi=300)
            plt.close()
        except Exception as e:
            print(f"Σφάλμα κατά τη δημιουργία γραφικού για Dst Port: {str(e)}")
            plt.close("all")

    if all(col in df.columns for col in ["Src Port", "Label"]):
        try:
            plt.figure(figsize=(12, 6))
            top_ports = df["Src Port"].value_counts().nlargest(10).index
            sns.countplot(
                data=df[df["Src Port"].isin(top_ports)],
                x="Src Port",
                hue="Label",
            )
            plt.title("Συχνότητα Ports Πηγής (Top 10)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join("stat_pics", "top_src_ports.png"), dpi=300)
            plt.close()
        except Exception as e:
            print(f"Σφάλμα κατά τη δημιουργία γραφικού για Src Port: {str(e)}")
            plt.close("all")

    if all(col in df.columns for col in ["Protocol", "Label"]):
        try:
            plt.figure(figsize=(12, 6))
            sns.countplot(data=df, x="Protocol", hue="Label")
            plt.yscale("log")
            plt.title("Κατανομή Πρωτοκόλλων")
            plt.tight_layout()
            plt.savefig(os.path.join("stat_pics", "protocol_dist.png"), dpi=300)
            plt.close()
        except Exception as e:
            print(f"Σφάλμα κατά τη δημιουργία γραφικού για Protocol: {str(e)}")
            plt.close("all")

    # 3. Συσχέτιση μεταβλητών - with existence checks
    if len(numeric_cols) > 5:
        try:
            plt.figure(figsize=(15, 10))
            corr_matrix = df[numeric_cols[:30]].corr()
            sns.heatmap(
                corr_matrix,
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                center=0,
                linewidths=0.5,
            )
            plt.title("Μητρώο Συσχέτισης Αριθμητικών Στηλών (Στήλες 1-30)")
            plt.tight_layout()
            plt.savefig(
                os.path.join("stat_pics", "correlation_matrix_1_30.png"),
                dpi=300,
            )
            plt.close()
        except Exception as e:
            print(f"Σφάλμα κατά τη δημιουργία μητρώου συσχέτισης: {str(e)}")
            plt.close("all")

        if len(numeric_cols) > 30:
            try:
                plt.figure(figsize=(24, 16))
                corr_matrix = df[numeric_cols[20:]].corr()
                sns.heatmap(
                    corr_matrix,
                    annot=True,
                    fmt=".2f",
                    cmap="coolwarm",
                    center=0,
                    linewidths=0.5,
                )
                plt.title(
                    "Μητρώο Συσχέτισης Αριθμητικών Στηλών (Στήλες 31-Τέλος)"
                )
                plt.tight_layout()
                plt.savefig(
                    os.path.join("stat_pics", "correlation_matrix_31_end.png"),
                    dpi=300,
                )
                plt.close()
            except Exception as e:
                print(f"Σφάλμα κατά τη δημιουργία μητρώου συσχέτισης: {str(e)}")
                plt.close("all")

    # 4. Ανάλυση Labels - with existence check
    if "Label" in df.columns:
        try:
            plt.figure()
            sns.countplot(
                y="Label", data=df, order=df["Label"].value_counts().index
            )
            plt.yscale("log")
            plt.title("Κατανομή Labels")
            plt.tight_layout()
            plt.savefig(
                os.path.join("stat_pics", "label_distribution.png"), dpi=300
            )
            plt.close()
        except Exception as e:
            print(f"Σφάλμα κατά τη δημιουργία γραφικού για Labels: {str(e)}")
            plt.close("all")


def detect_patterns(df):
    """#1.6 Ανίχνευση μοτίβων"""
    print("\n--- ΑΝΙΧΝΕΥΣΗ ΜΟΤΙΒΩΝ & ΣΥΣΧΕΤΙΣΕΩΝ ---")

    if {"Flow Duration", "Total Fwd Packet", "Total Bwd packets"}.issubset(
        df.columns
    ):
        print("\nΣυσχέτιση Διάρκειας Ροής και Πακέτων:")
        print(
            df[
                ["Flow Duration", "Total Fwd Packet", "Total Bwd packets"]
            ].corr()
        )

        plt.figure()
        sns.scatterplot(
            data=df,
            x="Total Fwd Packet",
            y="Total Bwd packets",
            hue="Protocol",
            alpha=0.6,
        )
        plt.xscale("log")
        plt.yscale("log")
        plt.title("Συσχέτιση Εμπρός και Πίσω Πακέτων ανά Πρωτόκολλο")
        plt.tight_layout()
        plt.savefig(
            os.path.join("stat_pics", "packets_correlation.png"), dpi=300
        )
        plt.close()

    tcp_flags = [
        "FIN Flag Count",
        "SYN Flag Count",
        "RST Flag Count",
        "PSH Flag Count",
        "ACK Flag Count",
        "URG Flag Count",
    ]
    if set(tcp_flags).issubset(df.columns):
        print("\nΣυσχέτιση TCP Flags:")
        print(df[tcp_flags].corr())

        plt.figure(figsize=(10, 8))
        sns.heatmap(df[tcp_flags].corr(), annot=True, cmap="coolwarm")
        plt.title("Συσχέτιση TCP Flags")
        plt.tight_layout()
        plt.savefig(
            os.path.join("stat_pics", "tcp_flags_correlation.png"), dpi=300
        )
        plt.close()

    if "Timestamp" in df.columns:
        try:
            df["Hour"] = pd.to_datetime(df["Timestamp"]).dt.hour
            plt.figure(figsize=(12, 6))
            sns.countplot(data=df, x="Hour", hue="Label")
            plt.yscale("log")
            plt.title("Κίνηση ανά Ώρα της Ημέρας")
            plt.tight_layout()
            plt.savefig(
                os.path.join("stat_pics", "traffic_by_hour.png"), dpi=300
            )
            plt.close()
        except:
            print("Could not parse Timestamp - skipping time analysis")


def main():
    """#1.7 Κύρια λειτουργία του προγράμματος"""
    # Δημιουργία φακέλων αν δεν υπάρχουν
    os.makedirs("stat_pics", exist_ok=True)
    os.makedirs("new_dataset", exist_ok=True)

    print("\n" + "=" * 50)
    print("ΕΡΓΑΛΕΙΟ ΑΝΑΛΥΣΗΣ ΔΕΔΟΜΕΝΩΝ".center(50))
    print("=" * 50)

    while True:
        show_menu()
        choice = input("Επιλέξτε αρχείο (1-5): ")

        if choice == "65":
            print("\nΤερματισμός προγράμματος...")
            break

        if choice not in ["1", "2", "3", "4", "5"]:
            print("\nΜη έγκυρη επιλογή. Παρακαλώ επιλέξτε 1-6.")
            continue

        data = load_data(choice, get_n_rows())
        if data is not None:
            analyze_columns(data)
            calculate_statistics(data)
            create_visualizations(data)
            detect_patterns(data)

            print("\n" + "=" * 50)
            print("ΑΝΑΛΥΣΗ ΟΛΟΚΛΗΡΩΘΗΚΕ ΕΠΙΤΥΧΩΣ!".center(50))
            print("=" * 50)

            cont = input("\nΘέλετε να συνεχίσετε με άλλο αρχείο; (y/n): ")
            if cont.lower() != "":
                print("\nΤερματισμός προγράμματος...")
                break


if __name__ == "__main__":
    main()
