using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Data.SQLite;
using System.Configuration;
using System.Diagnostics;

namespace FitQuest
{
    public partial class Map : Form
    {
        private Profile userProfile;
        private Level currentLevel;
        private Dictionary<Point, int> nodePositions;
        private int userProgressionLevel;
        private ToolTip toolTip;
        private MainMenu mainMenu;
        private String teamName;

        private void InitializeToolTip()
        {
            toolTip = new ToolTip();
        }
        public Map(String teamName, MainMenu mainmenu, Profile userProfile)
        {
            this.userProfile = userProfile;
            this.mainMenu = mainmenu;
            this.teamName = teamName;
            InitializeComponent();
            InitializeNodePositions();
            FetchUserProgressionLevel();
            InitializeToolTip();
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
            string query;
            if (teamName == "solo")
            {
                query = "SELECT level FROM Profiles WHERE id = '" + userProfile.id + "'";
            }
            else
            {
                query = "SELECT level FROM Teams WHERE team_id = '" + teamName + "'";
            }

            using (SQLiteConnection connection = new SQLiteConnection(connectionString))
            {
                SQLiteCommand command = new SQLiteCommand(query, connection);
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
                    Tag = levelNum,
                    FlatStyle = FlatStyle.Flat,
                    Enabled = true  //Keep all buttons enabled for mouse events
                };

                nodeButton.Click += NodeButton_Click;
                nodeButton.MouseEnter += NodeButton_MouseEnter;
                nodeButton.MouseLeave += NodeButton_MouseLeave;

                if (levelNum < userProgressionLevel)
                {
                    nodeButton.BackColor = Color.Green;
                }
                else if (levelNum == userProgressionLevel)
                {
                    nodeButton.BackColor = Color.Red;
                }
                else
                {
                    nodeButton.BackColor = Color.Gray;
                }

                pictureBox1.Controls.Add(nodeButton);
            }
        }



        private void NodeButton_Click(object sender, EventArgs e)
        {
            Button node = sender as Button;

            if (node != null)
            {
                if (node.BackColor == Color.Gray)
                {
                    MessageBox.Show("This level is locked. Complete the previous level to unlock it.", "Locked Level", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }

                if (int.TryParse(node.Tag.ToString(), out int levelNumber))
                {
                    if (levelNumber < userProgressionLevel)
                    {
                        MessageBox.Show($"Level {levelNumber} has already been completed.", "Completed Level", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        return;
                    }

                    try
                    {
                        currentLevel = new Level(levelNumber, teamName);
                        MessageBox.Show($"Level {currentLevel.Count} selected!\nEnemy: {currentLevel.EnemyName}\nHP: {currentLevel.CurrentEnemyHP}/{currentLevel.EnemyHP}\n\nClick on Commence Battle to start Combat!");
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
        }



        private Dictionary<Button, Color> originalColors = new Dictionary<Button, Color>();

        private void NodeButton_MouseEnter(object sender, EventArgs e)
        {
            Button node = sender as Button;
            if (node != null)
            {
                //Store the original color of the button
                if (!originalColors.ContainsKey(node))
                {
                    originalColors[node] = node.BackColor;
                }
                node.BackColor = Color.Blue;

                //Show tooltip based on the button's color
                if (originalColors[node] == Color.Green)
                {
                    toolTip.SetToolTip(node, "Level already completed");
                }
                else if (originalColors[node] == Color.Gray)
                {
                    toolTip.SetToolTip(node, "Level is Locked, complete the previous level to unlock");
                }
                else if (originalColors[node] == Color.Red)
                {
                    toolTip.SetToolTip(node, "Current level, ready to start");
                }
                else
                {
                    toolTip.SetToolTip(node, ""); //Clear tooltip for other colors
                }
            }
        }

        private void NodeButton_MouseLeave(object sender, EventArgs e)
        {
            Button node = sender as Button;
            if (node != null)
            {
                //Restore the original color of the button
                if (originalColors.ContainsKey(node))
                {
                    node.BackColor = originalColors[node];
                }
                toolTip.SetToolTip(node, "");
            }
        }




        private void button1_Click(object sender, EventArgs e)
        {
            
            if (currentLevel == null)
            { 
                MessageBox.Show($"Love the enthusiasm! \r\nBut you need to select a level first. Your current level is {userProgressionLevel}.", "Select Node", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return; 
            }

            MessageBox.Show("Initiating camera check...");

            //Simulate camera check (replace with actual webcam functionality)
            System.Threading.Thread.Sleep(300); 
            MessageBox.Show("Analyzing image...");

            System.Threading.Thread.Sleep(300);
            MessageBox.Show("User detected.");

            System.Threading.Thread.Sleep(300);
            MessageBox.Show("Ready to commence battle.");

            //Hide the current form (main menu)
            this.Hide();

            //Check if exercises are populated
            if (userProfile.AreExercisesPopulated)
            {
                //Show the combat form
                CombatSystem combatForm = new CombatSystem(mainMenu, userProfile, currentLevel, teamName);
                combatForm.Show();
            }
            else
            {
                //Show the training program form
                TrainingProgram trainingProgramForm = new TrainingProgram(mainMenu, userProfile, currentLevel, teamName);
                trainingProgramForm.Show();
            }
        }




        private void backButton_Click(object sender, EventArgs e)
        {
            this.mainMenu.Show();
            this.Hide();
        }

        private void Map_Load(object sender, EventArgs e)
        {

        }
    }
}
