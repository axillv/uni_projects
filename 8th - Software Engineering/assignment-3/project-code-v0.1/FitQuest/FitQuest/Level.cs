using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;
using System.Configuration;

namespace FitQuest
{
    public class Level
    {
        public int Count { get; private set; }
        public string EnemyName { get; private set; }
        public int EnemyHP { get; private set; }
        public int RewardGold { get; private set; }
        public int RewardPoints { get; private set; }
        public int LevelNum { get; private set; }
        public int IsCompleted { get; private set; }

        public Level(int count)
        {
            string connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            string query = "SELECT * FROM level WHERE count = @count";

            using (SQLiteConnection connection = new SQLiteConnection(connectionString))
            {
                SQLiteCommand command = new SQLiteCommand(query, connection);
                command.Parameters.AddWithValue("@count", count);
                connection.Open();

                using (SQLiteDataReader reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        this.Count = Convert.ToInt32(reader["count"]);
                        this.EnemyName = reader["enemy_name"].ToString();
                        this.EnemyHP = Convert.ToInt32(reader["enemy_hp"]);
                        this.RewardGold = Convert.ToInt32(reader["reward_gold"]);
                        this.RewardPoints = Convert.ToInt32(reader["reward_points"]);
                        this.LevelNum = count;
                        this.IsCompleted = Convert.ToInt32(reader["is_completed"]);
                    }
                    else
                    {
                        throw new Exception("Level not found");
                    }
                }
            }
        }

        public void MarkAsCompleted(string profileId)
        {
            this.IsCompleted = 1;
            UpdateLevelStatusInDatabase();
            UpdateProfileProgression(profileId);
        }

        private void UpdateLevelStatusInDatabase()
        {
            string connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            string query = "UPDATE level SET is_completed = @is_completed WHERE count = @count";

            using (SQLiteConnection connection = new SQLiteConnection(connectionString))
            {
                SQLiteCommand command = new SQLiteCommand(query, connection);
                command.Parameters.AddWithValue("@is_completed", this.IsCompleted);
                command.Parameters.AddWithValue("@count", this.Count);
                connection.Open();
                command.ExecuteNonQuery();
            }
        }

        private void UpdateProfileProgression(string profileId)
        {
            string connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            string query = "UPDATE Profiles SET level = @level WHERE profile_id = @profileId";

            using (SQLiteConnection connection = new SQLiteConnection(connectionString))
            {
                SQLiteCommand command = new SQLiteCommand(query, connection);
                command.Parameters.AddWithValue("@level", this.Count);
                command.Parameters.AddWithValue("@profileId", profileId);
                connection.Open();
                command.ExecuteNonQuery();
            }
        }
    }
}
