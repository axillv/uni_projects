
﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;
using System.Windows.Forms;
using System.Configuration;

namespace FitQuest
{
    public partial class Inventory : Form
    {

        private Profile userProfile;
        private string id;
        private int Gold;
        private bool accessedFromCombatSystem = false;

        public Inventory(Profile userProfile, bool accessedFromCombatSystem)
        {
            this.userProfile = userProfile;
            this.id = userProfile.id;
            this.Gold = userProfile.Gold;
            InitializeComponent();
            this.Load += new System.EventHandler(this.Inventory_Load);
            this.accessedFromCombatSystem = accessedFromCombatSystem;

        }

        private void Inventory_Load(object sender, EventArgs e)
        {
            LoadInventoryData();
            if (accessedFromCombatSystem)
            {
                button2.Visible = false;
                button6.Visible = false;
            }
        }

        public void LoadInventoryData()
        {
            string connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;

            using (SQLiteConnection connection = new SQLiteConnection(connectionString))
            {
                try
                {
                    connection.Open();
                    string query = "SELECT * FROM Inventory"; // Ensure this matches your table name
                    using (SQLiteCommand command = new SQLiteCommand(query, connection))
                    {
                        using (SQLiteDataReader reader = command.ExecuteReader())
                        {
                            listView1.Items.Clear();
                            while (reader.Read())
                            {
                                string name = reader["Name"].ToString();
                                string category = reader["Category"].ToString();
                                string description = reader["Description"].ToString();
                                string quantity = reader["Quantity"].ToString();
                                string value = reader["Value"].ToString();

                                ListViewItem item = new ListViewItem(name);
                                item.SubItems.Add(category);
                                item.SubItems.Add(description);
                                item.SubItems.Add(quantity);
                                item.SubItems.Add(value);
                                listView1.Items.Add(item);
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error: " + ex.Message);
                }
            }
        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (listView1.SelectedItems.Count > 0)
            {
                ListViewItem selectedItem = listView1.SelectedItems[0];
                textBox6.Text = selectedItem.SubItems[0].Text;
                textBox7.Text = selectedItem.SubItems[1].Text;
                textBox8.Text = selectedItem.SubItems[2].Text;
                textBox9.Text = selectedItem.SubItems[3].Text;
                textBox10.Text = selectedItem.SubItems[4].Text;
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (listView1.SelectedItems.Count > 0)
            {
                ListViewItem selectedItem = listView1.SelectedItems[0];
                string category = selectedItem.SubItems[1].Text;

                if (category == Item.categories.Consumable.ToString())
                {
                    MessageBox.Show("Please select a non-consumable item to equip.");
                }
                else
                {
                    int quantity = int.Parse(selectedItem.SubItems[3].Text);
                    string name = selectedItem.SubItems[0].Text; // Get the name of the item

                    MessageBox.Show($"You equipped: {name}");
                }
            }
        }

        private void button5_Click(object sender, EventArgs e)
        {
            if (listView1.SelectedItems.Count > 0 && listView1.SelectedItems[0].SubItems[1].Text == Item.categories.Consumable.ToString())
            {
                ListViewItem selectedItem = listView1.SelectedItems[0];
                int quantity = int.Parse(selectedItem.SubItems[3].Text);
                string name = selectedItem.SubItems[0].Text; // Get the name of the item

                if (quantity > 0)
                {
                    quantity--;
                    if (quantity == 0)
                    {
                        // Delete the item from the database
                        string deleteQuery = "DELETE FROM Inventory WHERE Name = @name AND Category = @category AND Description = @description";
                        ExecuteNonQuery(deleteQuery, selectedItem);
                        listView1.Items.Remove(selectedItem);
                    }
                    else
                    {
                        // Update the quantity in the database
                        string updateQuery = "UPDATE Inventory SET Quantity = @quantity WHERE Name = @name AND Category = @category AND Description = @description";
                        ExecuteNonQuery(updateQuery, selectedItem, quantity);
                        selectedItem.SubItems[3].Text = quantity.ToString();
                    }

                    MessageBox.Show($"You used: {name}");
        
                }
            }
            else
            {
                MessageBox.Show("Please select a consumable item to use.");
            }
        }

        private void button6_Click(object sender, EventArgs e)
        {
            if (listView1.SelectedItems.Count > 0)
            {
                ListViewItem selectedItem = listView1.SelectedItems[0];
                int quantity = int.Parse(selectedItem.SubItems[3].Text);
                int value = int.Parse(selectedItem.SubItems[4].Text);

                if (quantity > 0)
                {
                    quantity--;

                    if (quantity == 0)
                    {
                        // Delete the item from the database
                        string deleteQuery = "DELETE FROM Inventory WHERE Name = @name AND Category = @category AND Description = @description";
                        ExecuteNonQuery(deleteQuery, selectedItem);
                        listView1.Items.Remove(selectedItem);
                    }
                    else
                    {
                        // Update the quantity in the database
                        string updateQuery = "UPDATE Inventory SET Quantity = @quantity WHERE Name = @name AND Category = @category AND Description = @description";
                        ExecuteNonQuery(updateQuery, selectedItem, quantity);
                        selectedItem.SubItems[3].Text = quantity.ToString();
                    }

                    this.Gold += value;
                    string updateGoldQuery = "UPDATE Profiles SET gold = @gold WHERE id = @id";
                    UpdateUserGold(updateGoldQuery, this.id, this.Gold);

                    MessageBox.Show($"You just got {value} gold. Item sold successfully.");
                }
            }
        }
        private void ExecuteNonQuery(string query, ListViewItem item, int? quantity = null)
        {
            string connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            using (SQLiteConnection connection = new SQLiteConnection(connectionString))
            {
                connection.Open();
                using (SQLiteCommand command = new SQLiteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@name", item.SubItems[0].Text);
                    command.Parameters.AddWithValue("@category", item.SubItems[1].Text);
                    command.Parameters.AddWithValue("@description", item.SubItems[2].Text);
                    if (quantity.HasValue)
                    {
                        command.Parameters.AddWithValue("@quantity", quantity.Value);
                    }
                    command.ExecuteNonQuery();
                }
            }
        }

        private void UpdateUserGold(string query, string userId, int newGoldAmount)
        {
            string connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            using (SQLiteConnection connection = new SQLiteConnection(connectionString))
            {
                try
                {
                    connection.Open();
                    using (SQLiteCommand command = new SQLiteCommand(query, connection))
                    {
                        command.Parameters.AddWithValue("@gold", newGoldAmount);
                        command.Parameters.AddWithValue("@id", userId);
                        command.ExecuteNonQuery();
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error updating gold: " + ex.Message);
                }
            }
        }

        private void backButton_Click(object sender, EventArgs e)
        {

            MainMenu MainMenuForm = new MainMenu();
            MainMenuForm.Show();
            this.Hide();
        }
    }
}