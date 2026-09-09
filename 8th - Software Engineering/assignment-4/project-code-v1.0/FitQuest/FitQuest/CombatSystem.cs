using System;
using System.CodeDom;
using System.Collections;
using System.Configuration;
using System.Data;
using System.Data.SQLite;
using System.Drawing;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Linq;

namespace FitQuest
{
    public partial class CombatSystem : Form
    {
        private readonly Level currentLevel;
        private readonly int afkMaxSeconds = 10; // original 300
        private readonly int inactivityMaxSeconds = 5; // original 60
        private int inactivitySeconds = 0;
        // 0 is for afk timer, 1 is for waiting for activity
        private int inactiveTimerType = 0;
        
        private int combatTimeSeconds = 0;

        private Enemy combatEnemy;
        private string connectionString;

        private Profile userProfile;
        private MainMenu mainmenu;
        private String teamName;
        public CombatSystem(MainMenu mainmenu, Profile userProfile, Level currentLevel, String teamName)
        {
            InitializeComponent();

            // Enable double buffering
            this.SetStyle(ControlStyles.OptimizedDoubleBuffer | 
                          ControlStyles.AllPaintingInWmPaint | 
                          ControlStyles.UserPaint, true);
            this.UpdateStyles();


            this.teamName = teamName;
            this.userProfile = userProfile;
            this.mainmenu = mainmenu;
            this.connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            this.currentLevel = currentLevel;
            this.combatEnemy = new Enemy(currentLevel.EnemyName, currentLevel.EnemyHP, currentLevel.CurrentEnemyHP, currentLevel.LevelNum);

            //this.enemyHealthBar.Maximum = currentLevel.currentHP;
            updateEnemyInfo();
            this.nodeInfo.Text = getLevelInfo(currentLevel);
        }

        private void CombatSystem_Load(object sender, EventArgs e)
        {

            PopulateExerciseDataGrid();

            this.secondsPassedLabel.Text = "00:00";
            combatTimer.Interval = 1000;
            combatTimer.Start();

            characterInfoLabel.Text = userProfile.id + "(lvl. " + userProfile.Level + ")";

            inactivityTimer.Interval = 1000; // 1 second
            StartInactivityTimer(0);
        }

        private void PopulateExerciseDataGrid()
        {
            DataTable exerciseTable = new DataTable();
            exerciseTable.Columns.Add("Exercise Name", typeof(string));
            exerciseTable.Columns.Add("Sets", typeof(int));
            exerciseTable.Columns.Add("Repetitions", typeof(int));

            foreach (var program in userProfile.Exercises.Values)
            {
                foreach (string exercise in program)
                {
                    DataRow row = exerciseTable.NewRow();
                    row["Exercise Name"] = exercise;
                    row["Sets"] = 3; // Default sets
                    row["Repetitions"] = 10; // Default repetitions
                    exerciseTable.Rows.Add(row);
                }
            }

            exerciseDataGrid.DataSource = exerciseTable;
            exerciseDataGrid.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
        }

        public void useConsumable(ConsumableItemInstance consumable)
        {
            Hashtable hashtable = consumable.GetStats();
            // Get the first key-value pair
            if (hashtable.Count > 0)
            {
                DictionaryEntry firstEntry = hashtable.Cast<DictionaryEntry>().First();
                object Attr = firstEntry.Key;
                object AttrValue= firstEntry.Value;

                switch ((string)Attr)
                {
                    case "instantDamage":
                        dealDamageWrapper((int)AttrValue);
                        return;

                    default:
                        return;
                }

            }

        }

        private void updateEnemyInfo()
        {
            this.enemyHealthBar.Maximum = this.combatEnemy.maxHP;
            this.enemyHealthBar.Value = this.combatEnemy.currentHP;
            this.healthBarLabel.Text = this.enemyHealthBar.Value.ToString() + "/" + this.enemyHealthBar.Maximum.ToString();
            this.enemyNameLabel.Text = this.combatEnemy.EnemyName;
        }

        public void dealDamageWrapper(int damage)
        {
            this.combatEnemy.takeDamage(damage);
            updateEnemyInfo();
            if (this.combatEnemy.isDead())
            {
                victorySequence();
            }

        }

        private void attackButton_Click(object sender, EventArgs e)
        {
            StartInactivityTimer(0);
            if (exerciseDataGrid.SelectedRows.Count > 0)
            {
                // Simulate a detected repetition
                Repetition rep = new Repetition(1, 10);

                // Call function to calculate damage
                int damageDeal = calculateDamage(combatEnemy, userProfile, currentLevel, rep);
                dealDamageWrapper(damageDeal);


                //get the selected row
                DataGridViewRow selectedRow = exerciseDataGrid.SelectedRows[0];
                int repetitions = Convert.ToInt32(selectedRow.Cells["Repetitions"].Value);
                int sets = Convert.ToInt32(selectedRow.Cells["Sets"].Value);

                //reduce selected exercise's reps
                repetitions--;

                if (repetitions <= 0)
                {
                    //reduce set if done with the set's reps
                    sets--;
                    if (sets <= 0)
                    {
                        //remove exercise from the table when sets are done
                        exerciseDataGrid.Rows.Remove(selectedRow);
                    }
                    else
                    {
                        //restore reps if there are more sets
                        repetitions = 10;
                        selectedRow.Cells["Sets"].Value = sets;
                        selectedRow.Cells["Repetitions"].Value = repetitions;
                    }
                }
                else
                {
                    //update reps if reps there are more than 0
                    selectedRow.Cells["Repetitions"].Value = repetitions;
                }
            }
        }

        private void stopCombat()
        {
            combatTimer.Stop();
            inactivityTimer.Stop();
        }

        private void victorySequence()
        {
            stopCombat();
            userProfile.AreExercisesPopulated=false;
            userProfile.TimesTrained += 1;
            Rewards rewardsObj = calculateRewards();
            saveBattleRecord();
            saveRewardsToAccount(rewardsObj);
            showVictoryScreen(rewardsObj);
        }

        private void defeatSequence()
        {
            stopCombat();
            userProfile.AreExercisesPopulated = false;
            userProfile.TimesTrained += 1;
            saveBattleRecord();
            showDefeatScreen();
        }

        private bool saveBattleRecord() 
        {
            using (SQLiteConnection con = new SQLiteConnection(connectionString)) { 
                con.Open();
                // update current hp of enemy
                string query;
                if (this.teamName == "solo")
                {
                    query = "UPDATE Level SET enemy_current_hp = @enemyHP WHERE count = @levelCount";
                }
                else
                {
                    query = "UPDATE team_Level SET enemy_current_hp = @enemyHP WHERE count = @levelCount";
                }
                using (SQLiteCommand command = new SQLiteCommand(query, con))
                {
                    // Add the parameter and its value
                    command.Parameters.AddWithValue("@enemyHP", combatEnemy.currentHP);
                    command.Parameters.AddWithValue("@levelCount", currentLevel.Count);

                    // Execute the command
                    int rowsAffected = command.ExecuteNonQuery();

                    if (rowsAffected == 0) return false;
                }

                if (combatEnemy.currentHP == 0)
                {
                    // mark level as complete
                    if (this.teamName == "solo")
                    {
                        query = "UPDATE Level SET is_completed = 1 WHERE count = @levelCount";
                    }
                    else
                    {
                        query = "UPDATE team_Level SET is_completed = 1 WHERE count = @levelCount";
                    }
                    using (SQLiteCommand command = new SQLiteCommand(query, con))
                    {
                        // Add the parameter and its value
                        command.Parameters.AddWithValue("@levelCount", currentLevel.Count);

                        // Execute the command
                        int rowsAffected = command.ExecuteNonQuery();

                        if (rowsAffected == 0) return false;
                    }
                }
                return true;
            }
        }

        private bool isCamWorking()
        {
            return true;
        }



        // pass player or smth
        private Rewards calculateRewards()
        {
            // Given lvl and item bonuses get a "points value"
            // lvl + dayStreak
            int rewardPoints = 100;
            // divide that points value in various rewards (handled from rewards object)
            // rewards obj
            return new Rewards(100);
        }

        private void showVictoryScreen(Rewards rewardsObj)
        {
            // Create form or dim screen
            // from the reward obj passed show the rewards

            removeControls();

            VictoryScreen victoryScreen = new VictoryScreen(rewardsObj, combatEnemy.EnemyName);
            victoryScreen.Dock = DockStyle.Fill; // Set the Dock property to fill the form

            this.Controls.Add(victoryScreen);

        }

        private void removeControls()
        {
            // Suspend layout logic
            this.SuspendLayout();

            // Create form or dim screen
            foreach (Control ctrl in this.Controls)
            {
                if (ctrl.Visible)
                {
                    ctrl.Visible = false;
                }
            }

            // Resume layout logic
            this.ResumeLayout();
        }

        private void showDefeatScreen()
        {
            removeControls();

            DefeatScreen defeatScreen = new DefeatScreen(mainmenu, combatEnemy.currentHP);
            defeatScreen.Dock = DockStyle.Fill; // Set the Dock property to fill the form

            this.Controls.Add(defeatScreen);
        }

        private bool saveRewardsToAccount(Rewards rewardsObj)
        {
            // Save in database
            // connection

            using (SQLiteConnection con = new SQLiteConnection(connectionString))
            {
                con.Open();
                // add new gold
                string query = "UPDATE Profiles SET gold = gold + @goldGained WHERE ID = @playerID";
                using (SQLiteCommand command = new SQLiteCommand(query, con))
                {
                    // Add the parameter and its value
                    command.Parameters.AddWithValue("@goldGained", rewardsObj.getCurrency());
                    command.Parameters.AddWithValue("@playerID", userProfile.id);

                    // Execute the command
                    int rowsAffected = command.ExecuteNonQuery();

                    if (rowsAffected == 0) return false;
                }

                // update level of player
                if (this.teamName == "solo")
                {
                    query = "UPDATE Profiles SET level = level + 1 WHERE ID = '" + userProfile.id + "'";
                    Console.WriteLine(query);
                }
                else
                {
                    query = "UPDATE teams SET level = level + 1 WHERE team_id = '" + this.teamName + "'";
                    Console.WriteLine(query);
                }
                using (SQLiteCommand command = new SQLiteCommand(query, con))
                {
                    // Add the parameter and its value
                    command.Parameters.AddWithValue("@playerID", userProfile.id);

                    // Execute the command
                    int rowsAffected = command.ExecuteNonQuery();

                    if (rowsAffected == 0) return false;
                }

                if (this.teamName == "solo")
                    {
                        query = "UPDATE Level SET is_completed = 1 WHERE count = @levelCount";
                    }
                    else
                    {
                        query = "UPDATE team_Level SET is_completed = 1 WHERE count = @levelCount";
                    }

                using (SQLiteCommand command = new SQLiteCommand(query, con))
                {
                    // Add the parameter and its value
                    command.Parameters.AddWithValue("@levelCount", currentLevel.Count);

                    // Execute the command
                    int rowsAffected = command.ExecuteNonQuery();

                    if (rowsAffected == 0) return false;
                }


                // TODO: add new items


                // if successful return true
                return true;
            }
        }


        private string getLevelInfo(Level currentLevel)
        {
            if (currentLevel != null)
            {

                return "Dreary Desert " + "(lvl. " + currentLevel.LevelNum +")";
            }

            return "Dreary Desert " + "(lvl. " + 41 + ")";
        }


        private void StartInactivityTimer(int type)
        {
            afkCheckGroupBox.Visible = false;
            inactivityTimer.Stop();
            inactiveTimerType = type;
            inactivitySeconds = 0;
            inactivityTimer.Start();

            // show activity confirmation
            if (inactiveTimerType == 1)
            {
                afkCheckGroupBox.Visible = true;
            }
        }

        private int calculateDamage(Enemy enemyObj, Profile car, Level currentRoom, Repetition rep)
        {
            return rep.calculateDamage();
        }


        public static string FormatSecondsToMMSS(int totalSeconds)
        {
            TimeSpan timeSpan = TimeSpan.FromSeconds(totalSeconds);
            return timeSpan.ToString(@"mm\:ss");
        }

        private void combatTimer_Tick(object sender, EventArgs e)
        {
            this.combatTimeSeconds++;
            this.secondsPassedLabel.Text = FormatSecondsToMMSS(this.combatTimeSeconds);
        }

        // TODO: Tie inactivity to mouse clicks etc
        private void inactivityTimer_Tick(object sender, EventArgs e)
        {
            inactivitySeconds++;
            switch (this.inactiveTimerType)
            {
                // afk countdown
                case 0:
                    if (inactivitySeconds == afkMaxSeconds)
                    {
                        StartInactivityTimer(1);
                    }
                    break;

                case 1:
                    afkCheckButton.Text = "I'm here!\n(" + (inactivityMaxSeconds-inactivitySeconds) + "s left)";
                    if (inactivitySeconds == inactivityMaxSeconds)
                    {
                        defeatSequence();
                    }
                    break;

                default:
                    break;
            }

        }

        private void afkCheckButton_Click(object sender, EventArgs e)
        {
            // so he's here
            afkCheckGroupBox.Visible = false;
            StartInactivityTimer(0);
        }

        private void fleeButton_Click(object sender, EventArgs e)
        {
            defeatSequence();
        }

        private void inventoryButton_Click(object sender, EventArgs e)
        {
            Inventory inventoryForm = new Inventory(mainmenu, userProfile, true, this); // Indicate it's accessed from CombatSystem
            inventoryForm.LoadInventoryData(true);
            inventoryForm.Show();
        }

    }
}
