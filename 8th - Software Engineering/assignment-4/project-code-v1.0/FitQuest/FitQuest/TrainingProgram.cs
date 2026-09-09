using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Data.SQLite;
using System.Diagnostics;
using System.Linq;
using System.Windows.Forms;

namespace FitQuest
{
    public partial class TrainingProgram : Form
    {
        private int userAge;
        private int userLevel;
        string connectionString;
        private Profile userProfile;
        private Level currentLevel;
        private MainMenu mainmenu;
        private String teamName;

        public TrainingProgram(MainMenu mainmenu, Profile userProfile, Level currentLevel, String teamName)
        {
            this.mainmenu = mainmenu;
            this.teamName = teamName;
            //initialize connection
            this.connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            InitializeComponent();
            userAge = userProfile.Age;
            userLevel = userProfile.Level;
            this.userProfile = userProfile;
            if (userProfile.TimesTrained > 4)
            {
                createDangerWarning();
                //if user accepts ->getPrograms(), if not get him back to the main menu
            }

            //populate the buttons with exercise programs
            getPrograms();
            this.currentLevel = currentLevel;
        }

        public void createDangerWarning()
        {
            dangerWarningBox.Visible = true;
        }

        //buttons 1,2 and 3 choose push, pull and legs training programs respectively
        private void button1_Click(object sender, EventArgs e) 
        {
            chooseProgram("Push");
            CombatSystem CombatForm = new CombatSystem(mainmenu, userProfile, this.currentLevel, teamName);
            CombatForm.Show();
            this.Hide();
        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            chooseProgram("Pull");
            CombatSystem CombatForm = new CombatSystem(mainmenu, userProfile, this.currentLevel, teamName);
            CombatForm.Show();
            this.Hide();
        }

        private void button3_Click_1(object sender, EventArgs e)
        {
            chooseProgram("Legs");
            CombatSystem CombatForm = new CombatSystem(mainmenu, userProfile, this.currentLevel, teamName);
            CombatForm.Show();
            this.Hide();
        }
        public class Exercise
        {
            public string Name { get; set; }
        }
        private void getPrograms()
        {
            using (SQLiteConnection con = new SQLiteConnection(connectionString))
            {
                con.Open();
                string query = "SELECT * FROM TrainingProgram";
                SQLiteCommand cmd = new SQLiteCommand(query, con);
                DataTable dt = new DataTable();
                SQLiteDataAdapter adapter = new SQLiteDataAdapter(cmd);
                adapter.Fill(dt);


                var (pushExercises, pullExercises, legExercises) = calculateTrainingProgram(dt, userAge, userLevel);


                //convert exercise names to exercise objects
                List<Exercise> exercises = pushExercises.Select(ex => new Exercise { Name = ex }).ToList();
                //print them in the grid views
                dataGridView1.DataSource = exercises;

                exercises = pullExercises.Select(ex => new Exercise { Name = ex }).ToList();
                dataGridView2.DataSource = exercises;

                exercises = legExercises.Select(ex => new Exercise { Name = ex }).ToList();
                dataGridView3.DataSource = exercises;
            }
        }

        private (List<string> pushExercises, List<string> pullExercises, List<string> legExercises) calculateTrainingProgram(DataTable dt, int age, int level)
        {
            var pushExercises = new List<string>();
            var pullExercises = new List<string>();
            var legExercises = new List<string>();

            //filter exercises based on age and level (not implemented yet)
            foreach (DataRow row in dt.Rows)
            {
                string exerciseName = row["exercise_name"].ToString();
                string category = row["muscle"].ToString();

                //categorize exercises based on muscle category
                if (category == "Push")
                {
                    pushExercises.Add(exerciseName);
                }
                else if (category == "Pull")
                {
                    pullExercises.Add(exerciseName);
                }
                else if (category == "Legs")
                {
                    legExercises.Add(exerciseName);
                }
            }


            return (pushExercises, pullExercises, legExercises);
        }


        private void TrainingProgram_Load(object sender, EventArgs e)
        {

        }


        private void button4_Click(object sender, EventArgs e)
        {
            chooseProgram("makeOwnProgram");
        }

        private void chooseProgram(string text)  //this can be modified to it chooses programs based on age, level, weight etc.
            //update the userProfile's exercises with the selected program's exercises
        {
            if (text == "Push")
            {
                userProfile.Exercises["Push"] = (dataGridView1.DataSource as List<Exercise>)?.Select(ex => ex.Name).ToList();
            }
            else if (text == "Pull")
            {
                userProfile.Exercises["Pull"] = (dataGridView2.DataSource as List<Exercise>)?.Select(ex => ex.Name).ToList();
            }
            else if (text == "Legs")
            {
                userProfile.Exercises["Legs"] = (dataGridView3.DataSource as List<Exercise>)?.Select(ex => ex.Name).ToList();
            }
            else if (text == "makeOwnProgram")
            {
                createProgramMaker();
            }
            else if (text == "choosePastProgram")
            {
                
            }
        }

        private void createProgramMaker()
        {
            groupBox1.Visible = false;
            groupBox2.Visible = true;

            PopulateProgramMakerExercises();
        }

        private void PopulateProgramMakerExercises()     //populates the datagridview with the database's exercises
        {
            using (SQLiteConnection con = new SQLiteConnection(connectionString))
            {
                con.Open();
                string query = "SELECT * FROM TrainingProgram";      //get all the exercises from the database
                SQLiteCommand cmd = new SQLiteCommand(query, con);
                DataTable dt = new DataTable();
                SQLiteDataAdapter adapter = new SQLiteDataAdapter(cmd);
                adapter.Fill(dt);

                List<Exercise> exercises = dt.AsEnumerable()       //make the list from the retrieved dataset
                                             .Select(row => new Exercise { Name = row["exercise_name"].ToString() })
                                             .ToList();
                dataGridView4.DataSource = exercises;
            }
        }

        private void buttonSaveProgram_Click_1(object sender, EventArgs e)   //button "Save Program", saves the selected exercises
        {
            var selectedExercises = dataGridView4.SelectedRows
                                        .OfType<DataGridViewRow>()
                                        .Select(row => row.DataBoundItem as Exercise)
                                        .ToList();

            if (selectedExercises.Any())
            {
                userProfile.Exercises["Custom"] = selectedExercises.Select(ex => ex.Name).ToList();    //sets the userprofile's exercises
                MessageBox.Show("Custom program saved successfully!");
                CombatSystem CombatForm = new CombatSystem(mainmenu, userProfile, this.currentLevel, teamName);
                CombatForm.Show();
                this.Hide();
            }
            else
            {
                MessageBox.Show("Please select at least one exercise.");
            }
        }

        private void button5_Click(object sender, EventArgs e)
        {
            if (userProfile.Exercises.ContainsKey("Custom") && userProfile.Exercises["Custom"].Any())
            {
                groupBox1.Visible = false;
                groupBox3.Visible = true;
                var customExercises = userProfile.Exercises["Custom"]
                                                  .Select(ex => new Exercise { Name = ex })
                                                  .ToList();

                dataGridView5.DataSource = customExercises;
            }
            else
            {
                MessageBox.Show("No custom program found.");
            }
        }

        private void selectpastprogramButton_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Custom program saved successfully!");
            CombatSystem CombatForm = new CombatSystem(mainmenu, userProfile, this.currentLevel, teamName);
            CombatForm.Show();
            this.Hide();
        }

        private void acceptWarning_Click(object sender, EventArgs e)
        {
            dangerWarningBox.Visible = false;
        }

        private void declineDanger_Click(object sender, EventArgs e)
        {
            mainmenu.Show();
            this.Hide();
        }
    }

    
}