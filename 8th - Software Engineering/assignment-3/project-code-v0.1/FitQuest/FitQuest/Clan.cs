using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Configuration;
using System.Data;
using System.Data.SQLite;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FitQuest
{
    public partial class Clan : Form
    {
        string connectionString;
        private Profile userProfile;
        private string team_id;
        private SQLiteConnection connection;
        bool hasInternetConnectionBool;


        public Clan(Profile userProfile)
        {
            //initialize connection and components
            this.connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            this.connection = new SQLiteConnection(connectionString); // Initialize the connection
            this.hasInternetConnectionBool = hasInternetConnection();

            InitializeComponent();
            this.userProfile = userProfile;
            this.team_id = userProfile.Team_id;
            

            //check if team_id is null
            //if (true)
            if (string.IsNullOrEmpty(this.team_id))       
            {
                notinaclanPanel.Visible = true;
                createaclanPanel.Visible = false;
                //show team making menu
            }
            else
            {
                //load clan details if team_id is not null (user is in a clan)
                if (hasInternetConnectionBool)
                {
                    LoadClanCamp();

                }
                else { MessageBox.Show("Please connect to the internet first"); }

            }
        }

        private void LoadClanCamp()
        {
            //load the clan camp
            clancampPanel.Visible = true;
            clannamecampLabel.Text = "Clan's " + team_id + " Camp";
           
            string query = "SELECT * FROM Profiles WHERE team_id == '" + team_id + "';";
            SQLiteCommand cmd = new SQLiteCommand(query, connection);

            //dataTable to hold the data of the clan members
            DataTable dt = new DataTable();
            SQLiteDataAdapter adapter = new SQLiteDataAdapter(cmd);
            adapter.Fill(dt);

            //populate the grid with the clan's members
            clanmembersGrid.DataSource = dt;

        }

        private void backButton_Click(object sender, EventArgs e)
        {
            //leaves the clan camp
            MainMenu MainMenuForm = new MainMenu();
            MainMenuForm.Show();
            this.Hide();
        }


        private void confirmcreateButton_Click_1(object sender, EventArgs e)
        {
            createClan();

        }
        private void createClan()
        {
            string teamName = clannameTextBox.Text.Trim(); // Get the team name from the textbox
            bool formGood = false;
            connection.Open();
            formGood = checkForm(teamName);
            if (formGood)
            {

                string updateQuery = $"UPDATE Profiles SET team_id = @TeamID WHERE id = '" + userProfile.id + "';";

                using (SQLiteCommand updateCommand = new SQLiteCommand(updateQuery, connection))
                {
                    updateCommand.Parameters.AddWithValue("@TeamID", teamName);
                    updateCommand.ExecuteNonQuery();
                }

                string insertQuery = "INSERT INTO teams (team_id) VALUES ('" + teamName + "');";

                using (SQLiteCommand insertCommand = new SQLiteCommand(insertQuery, connection))
                {
                    insertCommand.ExecuteNonQuery();
                }


                invitefriendspanel.Visible = true;
                createaclanPanel.Visible = false;

                // SQL query to get friends
                string query = "SELECT * FROM Friends";
                SQLiteCommand cmd = new SQLiteCommand(query, connection);

                // DataTable to hold the data
                DataTable dt = new DataTable();
                SQLiteDataAdapter adapter = new SQLiteDataAdapter(cmd);
                adapter.Fill(dt);

                // Add a CheckBox column to the DataTable
                DataColumn selectColumn = new DataColumn("Select", typeof(bool));
                dt.Columns.Add(selectColumn);

                // Set the DataSource of the DataGridView
                dataGridView1.DataSource = dt;

                // Set DataGridView properties for the checkbox
                dataGridView1.Columns["Select"].DisplayIndex = 0;
                dataGridView1.Columns["Select"].HeaderText = "Select";
                connection.Close();

            }
        }
    

        private bool checkForm(string teamName)
        {
            //check if a team name has been inputted
            if (string.IsNullOrWhiteSpace(teamName))
            {
                // Show an error message or handle the empty name case as needed
                MessageBox.Show("Please enter a valid team name.");
                return false;
            }

          

            //sQL command to check if the team name exists in the teams table
            string query = "SELECT COUNT(*) FROM teams WHERE team_id = '" + teamName + "';";

            //create and execute the command
            using (SQLiteCommand command = new SQLiteCommand(query, connection))
            {
                //add parameter for the team id
                command.Parameters.AddWithValue("@TeamID", teamName);

                // Execute the query
                int count = Convert.ToInt32(command.ExecuteScalar());
                // If count is greater than 0, it means the name already exists
                if (count > 0)
                {
                    MessageBox.Show("The name is already taken.");
                    return false;
                }
                else
                {
                    this.team_id = teamName;
                    return true;
                }
            }
        }


        private void createaclanbutton_Click_1(object sender, EventArgs e)
        {
            notinaclanPanel.Visible = false;
            createaclanPanel.Visible = true;
        }


        private void invitedoneButton_Click(object sender, EventArgs e)
        { 
            //initialize a list to keep selected names
            List<string> selectedNames = new List<string>();

            //loop through the DataGridView rows
            foreach (DataGridViewRow row in dataGridView1.Rows)
            {
                //check if the CheckBox is selected
                if (row.Cells["Select"].Value != DBNull.Value && row.Cells["Select"].Value != null)
                {
                    //get the friend's name and add to the list
                    string name = row.Cells["friendID"].Value.ToString(); //adjust column name as necessary
                    selectedNames.Add(name);
                }
            }

            //convert the list of names to a single string
            string selectedNamesString = string.Join(", ", selectedNames);

            insertIntoTeam(selectedNamesString);
            invitefriendspanel.Visible = false;
            LoadClanCamp();
        }

        private void insertIntoTeam(string Names)
        {

        }

        private void joinaclanButton_Click(object sender, EventArgs e)
        {
            joinaclanPanel.Visible = true;
            notinaclanPanel.Visible = false;

            //sql
            string query = "SELECT * FROM Friends WHERE clanID != 'null'";
            SQLiteCommand cmd = new SQLiteCommand(query, connection);

            //dataTable to hold the data
            DataTable dt = new DataTable();
            SQLiteDataAdapter adapter = new SQLiteDataAdapter(cmd);
            adapter.Fill(dt);


            //set the DataSource of the DataGridView
            dataGridView3.DataSource = dt;
            dataGridView3.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
        }




        private void jointheclanButton_Click(object sender, EventArgs e)
        {
            //check if any row is selected
            if (dataGridView3.SelectedRows.Count > 0)
            {
                jointheclan();
            }
            else //case where button is pressed without any friend selected
            {
                MessageBox.Show("Please select a friend.");
            }
        }

        private void jointheclan()
        {
            //get the value of the the clan name
            string clanName = dataGridView3.SelectedRows[0].Cells[1].Value.ToString();
            MessageBox.Show($"You have joined: {clanName}");
            joinaclanPanel.Visible = false;
            this.team_id = clanName;
            LoadClanCamp();
        }
        private bool hasInternetConnection()
        {
            return true;
        }

        private void leaveclanButton_Click(object sender, EventArgs e)
        {
            //confirm if the user wants to leave the clan
            var confirmResult = MessageBox.Show("Are you sure you want to leave the clan?", "Confirm Leave Clan", MessageBoxButtons.YesNo);
            if (confirmResult == DialogResult.Yes)
            {
                using (var connection = new SQLiteConnection(connectionString))
                {
                    try
                    {
                        //update the database
                        connection.Open();
                        string updateQuery = "UPDATE Profiles SET team_id = NULL WHERE id = @UserID;";

                        using (var cmd = new SQLiteCommand(updateQuery, connection))
                        {
                            cmd.Parameters.AddWithValue("@UserID", userProfile.id);
                            cmd.ExecuteNonQuery();
                        }

                        //update the user profile and UI
                        this.team_id = null;
                        userProfile.UpdateTeamId(null);

                        //hide clan camp and show the panel for creating/joining a clan
                        clancampPanel.Visible = false;
                        notinaclanPanel.Visible = true;
                        createaclanPanel.Visible = false;

                        MessageBox.Show("You have left the clan.");
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Error leaving the clan: " + ex.Message);
                    }
                    finally
                    {
                        connection.Close();
                    }
                }
            }
        }

        private void Clan_Load(object sender, EventArgs e)
        {

        }

        private void teambattleButton_Click(object sender, EventArgs e)
        {
            // Hide the current form (main menu)
            this.Hide();

            // Check if exercises are populated
            if (userProfile.AreExercisesPopulated())
            {
                Console.WriteLine("Training program is chosen:");
                foreach (var category in userProfile.Exercises.Keys)
                {
                    Console.WriteLine($"{category} exercises: {string.Join(", ", userProfile.Exercises[category])}");
                }
                // Show the combat form
                CombatSystem combatForm = new CombatSystem(userProfile);
                combatForm.Show();
            }
            else
            {
                Console.WriteLine("Training program not chosen");
                this.Hide();
                TrainingProgram trainingProgramForm = new TrainingProgram(userProfile);
                trainingProgramForm.Show();
            }
        }
    }
}

