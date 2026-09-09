using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Data.SQLite;
using System.Configuration;

namespace FitQuest
{
    public partial class Map : Form
    {
        private Profile userProfile;
        private Level currentLevel;
        private Dictionary<Point, int> nodePositions;
        private int userProgressionLevel;

        public Map(Profile userProfile)
        {
            this.userProfile = userProfile;
            InitializeComponent();
            InitializeNodePositions();
            FetchUserProgressionLevel();
            CreateNodes();
        }

        private void InitializeNodePositions()
        {
            nodePositions = new Dictionary<Point, int>
            {
                { new Point(700, 500), 1 },
                { new Point(462, 519), 2 },
                { new Point(192, 532), 3 },
                { new Point(80, 430), 4 },
                { new Point(342, 367), 5 },
                { new Point(618, 354), 6 },
                { new Point(560, 234), 7 },
                { new Point(345, 265), 8 },
                { new Point(71, 250), 9 },
                { new Point(115, 95), 10 },
                { new Point(315, 79), 11 },
                { new Point(498, 46), 12 }
            };
        }

        private void FetchUserProgressionLevel()
        {
            string connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            string query = "SELECT level FROM Profiles WHERE id = @profileId";

            using (SQLiteConnection connection = new SQLiteConnection(connectionString))
            {
                SQLiteCommand command = new SQLiteCommand(query, connection);
                command.Parameters.AddWithValue("@profileId", userProfile.id);
                connection.Open();

                userProgressionLevel = Convert.ToInt32(command.ExecuteScalar());
            }
        }

        private void CreateNodes()
        {
            foreach (var entry in nodePositions)
            {
                Point pos = entry.Key;
                int levelNum = entry.Value;

                Button nodeButton = new Button
                {
                    Size = new Size(30, 30),
                    Location = pos,
                    Tag = levelNum, // Ensure Tag is set to an integer
                    
                    FlatStyle = FlatStyle.Flat
                };

                nodeButton.Click += NodeButton_Click;
                nodeButton.MouseEnter += NodeButton_MouseEnter;
                nodeButton.MouseLeave += NodeButton_MouseLeave;

                if (levelNum <= userProgressionLevel)
                {
                    nodeButton.BackColor = Color.Green;
                    nodeButton.Enabled = true;
                }
                else if (levelNum == userProgressionLevel + 1)
                {
                    nodeButton.BackColor = Color.Red;
                    nodeButton.Enabled = true;
                }
                else
                {
                    nodeButton.BackColor = Color.Gray;
                    nodeButton.Enabled = false;
                }

                pictureBox1.Controls.Add(nodeButton);
            }
        }

        private void NodeButton_Click(object sender, EventArgs e)
        {
            Button node = sender as Button;

                if (int.TryParse(node.Tag.ToString(), out int levelNumber))
                {
                    try
                    {
                        currentLevel = new Level(levelNumber);
                        MessageBox.Show($"Level {currentLevel.Count} selected!\nEnemy: {currentLevel.EnemyName}\nHP: {currentLevel.EnemyHP}\n\nClick on Commence Battle to start Combat!");
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error: {ex.Message}");
                    }
                }
                else
                {
                    MessageBox.Show("Invalid level number.");
                }
        }

        private Dictionary<Button, Color> originalColors = new Dictionary<Button, Color>();

        private void NodeButton_MouseEnter(object sender, EventArgs e)
        {
            Button node = sender as Button;
            if (node != null && node.Enabled)
            {
                // Store the original color of the button
                originalColors[node] = node.BackColor;
                node.BackColor = Color.Blue;
            }
        }

        private void NodeButton_MouseLeave(object sender, EventArgs e)
        {
            Button node = sender as Button;
            if (node != null && node.Enabled)
            {
                // Restore the original color of the button
                if (originalColors.ContainsKey(node))
                {
                    node.BackColor = originalColors[node];
                }
                else
                {
                    // Fallback to default color if the original color is not stored
                    node.BackColor = Color.Green;
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
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
                CombatSystem combatForm = new CombatSystem(userProfile, currentLevel);
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

        private void backButton_Click(object sender, EventArgs e)
        {
            MainMenu mainMenuForm = new MainMenu();
            mainMenuForm.Show();
            this.Hide();
        }
    }
}
