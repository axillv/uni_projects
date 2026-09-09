using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.SQLite;

using System.Configuration;
using System.Runtime.CompilerServices;

namespace FitQuest
{
    public partial class FriendsList : Form
    {
        private int rowIndex;
        string connectionString;
        bool hasInternetConnectionBool;
        private Profile userProfile;
        private MainMenu mainmenu;
        public FriendsList(MainMenu mainmenu, Profile userProfile)
        {
            this.connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;
            this.mainmenu = mainmenu;
            InitializeComponent();

            this.hasInternetConnectionBool = userProfile.hasInternetConnection();


            // Attach the event handler to the Load event of the form
            this.Load += FriendsList_Load;

            this.userProfile = userProfile;

            if (this.userProfile.Team_id == null)
            {
                friendsTabMenuStrip.Items[0].Enabled = false;
            }
        }

        private void FriendsList_Load(object sender, EventArgs e)
        {
            if (this.hasInternetConnectionBool)
            {
                fetchFriendsList(false);
            }
            else
            {
                fetchFriendsList(true);
            }

        }

        private void fetchFriendsList(bool cached = false)
        {
            // read only
            if (cached)
            {
                AddFriend.Visible = false;
                friendsTabMenuStrip.Visible = false;
                friendRequestsMenuStrip.Visible = false;
            }
            else
            {
                // connection
                using (SQLiteConnection con = new SQLiteConnection(connectionString))
                {
                    con.Open();
                    // friends list
                    string query = "SELECT playerID2 as 'Friend ID' FROM Friends WHERE playerID1=@playerID OR playerID2=@playerID";
                    using (SQLiteCommand command = new SQLiteCommand(query, con))
                    {
                        // Add the parameter and its value
                        command.Parameters.AddWithValue("@playerID", userProfile.id);

                        // data
                        DataTable friendsListTable = new DataTable();
                        SQLiteDataAdapter adapter = new SQLiteDataAdapter(command);
                        adapter.Fill(friendsListTable);

                        dataGridView1.DataSource = friendsListTable;
                        dataGridView1.ColumnHeadersHeight = 23;
                    }

                    // pending requests
                    string query2 = "SELECT senderID as 'Player ID' FROM PendingFriendRequests WHERE receiverID=@receiverID";
                    using (SQLiteCommand command2 = new SQLiteCommand(query2, con))
                    {
                        // Add the parameter and its value
                        command2.Parameters.AddWithValue("@receiverID", userProfile.id);

                        // Execute the command
                        int rowsAffected = command2.ExecuteNonQuery();

                        //if (rowsAffected == 0) return false;
                        // data
                        DataTable pendingIncomingTable = new DataTable();
                        SQLiteDataAdapter adapter2 = new SQLiteDataAdapter(command2);
                        adapter2.Fill(pendingIncomingTable);
                        dataGridView2.DataSource = pendingIncomingTable;
                        dataGridView2.ColumnHeadersHeight = 23;
                    }


                    // sent requests
                    string query3 = "SELECT receiverID as 'Player ID' FROM PendingFriendRequests WHERE senderID=@senderID";
                    using (SQLiteCommand command3 = new SQLiteCommand(query3, con))
                    {
                        // Add the parameter and its value
                        command3.Parameters.AddWithValue("@senderID", userProfile.id);

                        // Execute the command
                        int rowsAffected = command3.ExecuteNonQuery();

                        //if (rowsAffected == 0) return false;
                        // data
                        DataTable pendingSentTable = new DataTable();
                        SQLiteDataAdapter adapter3 = new SQLiteDataAdapter(command3);
                        adapter3.Fill(pendingSentTable);
                        sentRequestsGridView.DataSource = pendingSentTable;
                        sentRequestsGridView.ColumnHeadersHeight = 23;
                    }
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {

        }

        private void friendsListBox_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void LoadFriends_Click(object sender, EventArgs e)
        {

        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private bool sendFriendReq(string friendName)
        {
            // network success
            return true;
        }

        private void btnSendRequest_Click(object sender, EventArgs e)
        {
            string friendName = txtFriendName.Text;

            if (!string.IsNullOrEmpty(friendName))
            {
                if (sendFriendReq(friendName))
                {
                    lblResult.Text = "Friend request sent!";
                }
                else
                {
                    lblResult.Text = "Couldn't send friend request!";
                }
            }
            else
            {
                lblResult.Text = "Player doesn't exist!";
            }
        }

        private void AddFriend_Click(object sender, EventArgs e)
        {
            // toggle
            if (lblNamePrompt.Visible)
            {
                lblNamePrompt.Visible = false;
                txtFriendName.Visible = false;
                btnSendRequest.Visible = false;
                lblResult.Visible = false;
                lblfriendLink.Visible = false;
                txtfriendLink.Visible = false;
                buttonGenerateFriendLink.Visible = false;

            }
            else
            {

                // reset previous entries
                lblResult.Text = "";
                txtfriendLink.Text = "";

                lblNamePrompt.Visible = true;
                txtFriendName.Visible = true;
                btnSendRequest.Visible = true;
                lblResult.Visible = true;
                lblfriendLink.Visible = true;
                txtfriendLink.Visible = true;
                buttonGenerateFriendLink.Visible = true;
            }
        }

        private void FriendsTab_Click(object sender, EventArgs e)
        {

        }

        private void lblfriendLink_Click(object sender, EventArgs e)
        {

        }

        private void txtfriendLink_TextChanged(object sender, EventArgs e)
        {

        }

        private void buttonGenerateFriendLink_Click(object sender, EventArgs e)
        {
            txtfriendLink.Text = generateLink();
        }

        private string generateLink()
        {
            string basicLink = "fit.quest/";
            string randomUrl = "";
            randomUrl += GetLetter().ToString();

            return basicLink + randomUrl;
        }

        public static string GetLetter()
        {
            string chars = "@!abcdefghijklmnopqrstuvwxyz1234567890?ABCDEFGHIJKLMNOPQRSTUVWXYZ&";
            Random rand = new Random();
            StringBuilder result = new StringBuilder();
            for (int i = 0; i < 6; i++)
            {
                int num = rand.Next(0, chars.Length);
                result.Append(chars[num]);
            }
            return result.ToString();
        }

        private void dataGridView2_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {


        }

        private void friendsTabMenuStrip_Opening(object sender, CancelEventArgs e)
        {

        }

        private void btnGoBack_Click(object sender, EventArgs e)
        {
            // Hide the current form (main menu)
            this.Hide();

            // Show the menu form
            mainmenu.Show();
        }

        private void dataGridView1_CellFormatting(object sender, DataGridViewCellFormattingEventArgs e)
        {
            /* // TODO: Add activity icon
            // Check if the current column is the "activity" column and the value is "online"
            if (dataGridView1.Columns[e.ColumnIndex].Name == "activity" && e.Value.ToString() == "online")
            {
                // Load a green icon
                Image greenIcon = Properties.Resources.GreenIcon; // Assuming you have an icon named GreenIcon in your resources

                // Set the cell's icon
                e.Value = greenIcon;
            }
            */
        }

        private bool inviteFriendToTeam(string friendName)
        {
            return true;
        }

        private bool RespondIncomingFriendRequest(string friendName, bool accept)
        {
            // connection
            using (SQLiteConnection con = new SQLiteConnection(connectionString))
            {
                con.Open();
                // remove incoming friend req
                // query
                string query = "DELETE FROM PendingFriendRequests WHERE receiverID = @receiverID AND senderID = @senderID";
                using (SQLiteCommand command = new SQLiteCommand(query, con))
                {
                    // Add the parameter and its value
                    command.Parameters.AddWithValue("@receiverID", userProfile.id);
                    command.Parameters.AddWithValue("@senderID", friendName);

                    // Execute the command
                    int rowsAffected = command.ExecuteNonQuery();

                    if (rowsAffected == 0) return false;
                }

                if (accept)
                {
                    // add to friend
                    // query
                    query = "INSERT INTO Friends VALUES (@playerID, @friendID)";
                    using (SQLiteCommand command = new SQLiteCommand(query, con))
                    {
                        // Add the parameter and its value
                        command.Parameters.AddWithValue("@playerID", userProfile.id);
                        command.Parameters.AddWithValue("@friendID", friendName);

                        // Execute the command
                        int rowsAffected = command.ExecuteNonQuery();

                        if (rowsAffected == 0) return false;
                    }
                }
            }

            return true;
        }

        private bool deleteFriend(string friendName)
        {
            // connection
            using (SQLiteConnection con = new SQLiteConnection(connectionString))
            {
                con.Open();
                // remove friend
                // query
                string query = "DELETE FROM Friends WHERE (playerID1 = @friendID AND playerID2 = @playerID) or (playerID1 = @playerID AND playerID2 = @friendID)";
                using (SQLiteCommand command = new SQLiteCommand(query, con))
                {
                    // Add the parameter and its value
                    command.Parameters.AddWithValue("@friendID", friendName);
                    command.Parameters.AddWithValue("@playerID", userProfile.id);

                    // Execute the command
                    int rowsAffected = command.ExecuteNonQuery();

                    if (rowsAffected == 0) return false;
                }
            }

            return true;
        }

        private void displayFriendActionSuccess(string action, string friendName)
        {
            switch (action)
            {
                case "clan":
                    SuccessFriendActionLabel.Visible = true;
                    SuccessFriendActionLabel.Text = "You invited " + friendName + " to your clan!";
                    break;

                case "delete":
                    SuccessFriendActionLabel.Visible = true;
                    SuccessFriendActionLabel.Text = "You removed " + friendName + " from your friends list!";
                    break;

                case "decline":
                    SuccessFriendActionLabel.Visible = true;
                    SuccessFriendActionLabel.Text = "You declined " + friendName + "'s friend request."; 

                    break;

                case "accept":
                    SuccessFriendActionLabel.Visible = true;
                    SuccessFriendActionLabel.Text = "You accepted " + friendName + "'s friend request.";
                    break;

                case "error":
                    SuccessFriendActionLabel.Visible = true;
                    SuccessFriendActionLabel.Text = "Error occured.";
                    break;

                default:
                    break;
            }
        }

        private void friendsTabMenuStrip_ItemClicked(object sender, ToolStripItemClickedEventArgs e)
        {
            int columnIndex = 0; // friendid

            // Check if the row index is valid
            if (rowIndex >= 0 && rowIndex < dataGridView1.Rows.Count)
            {
                // Access the row at the specified index
                DataGridViewRow row = dataGridView1.Rows[rowIndex];

                // Check if the column index is valid
                if (columnIndex >= 0 && columnIndex < row.Cells.Count)
                {
                    // Access the cell at the specified column index
                    DataGridViewCell cell = row.Cells[columnIndex];

                    // Retrieve the value of the cell
                    object cellValue = cell.Value;
                    string friendName = (string)cellValue;
                    switch (e.ClickedItem.Text)
                    {
                        case "Invite to clan":
                            // pass friendName from datagridview when clicked
                            inviteFriendToTeam(friendName);
                            displayFriendActionSuccess("clan", friendName);
                            break;

                        case "Remove friend":
                            // pass friendName from datagridview when clicked
                            if (deleteFriend(friendName))
                            {
                                fetchFriendsList(false);
                                displayFriendActionSuccess("delete", friendName);
                            }
                            else
                            {
                                displayFriendActionSuccess("error", friendName);
                            }
                            break;

                        default:
                            break;
                    }
                }
            }


        }

        private void FriendsTab_SelectedIndexChanged(object sender, EventArgs e)
        {
            // reset info label
            SuccessFriendActionLabel.Visible = false;
            SuccessFriendActionLabel.Text = "";
        }

        private void dataGridView1_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                DataGridView.HitTestInfo hit = dataGridView1.HitTest(e.X, e.Y);
                if (hit.Type == DataGridViewHitTestType.Cell)
                {
                    rowIndex = hit.RowIndex;
                }
            }
        }

        private void contextMenuStrip1_Opening(object sender, CancelEventArgs e)
        {

        }

        private void friendRequestsMenuStrip_ItemClicked(object sender, ToolStripItemClickedEventArgs e)
        {
            int columnIndex = 0; // friendid

            // Check if the row index is valid
            if (rowIndex >= 0 && rowIndex < dataGridView2.Rows.Count)
            {
                // Access the row at the specified index
                DataGridViewRow row = dataGridView2.Rows[rowIndex];

                // Check if the column index is valid
                if (columnIndex >= 0 && columnIndex < row.Cells.Count)
                {
                    // Access the cell at the specified column index
                    DataGridViewCell cell = row.Cells[columnIndex];

                    // Retrieve the value of the cell
                    object cellValue = cell.Value;
                    string friendName = (string)cellValue;

                    switch (e.ClickedItem.Text)
                    {
                        case "Accept friend request":
                            // pass friendName from datagridview when clicked
                            if (RespondIncomingFriendRequest(friendName, true))
                            {
                                fetchFriendsList(false);
                                displayFriendActionSuccess("accept", friendName);
                            }
                            else
                            {
                                displayFriendActionSuccess("error", friendName);
                            }
                            break;

                        case "Decline friend request":
                            // pass friendName from datagridview when clicked
                            if (RespondIncomingFriendRequest(friendName, false))
                            {
                            fetchFriendsList(false);
                            displayFriendActionSuccess("decline", friendName);
                            }
                            else
                            {
                                displayFriendActionSuccess("error", friendName);
                            }
                            break;

                        default:
                            break;
                    }



                }
            }
        }

        private void dataGridView2_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                DataGridView.HitTestInfo hit = dataGridView1.HitTest(e.X, e.Y);
                if (hit.Type == DataGridViewHitTestType.Cell)
                {
                    rowIndex = hit.RowIndex;
                }
            }
        }

        private void sentRequestsGridView_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                DataGridView.HitTestInfo hit = dataGridView1.HitTest(e.X, e.Y);
                if (hit.Type == DataGridViewHitTestType.Cell)
                {
                    rowIndex = hit.RowIndex;
                }
            }
        }

        private bool removeSentFriendRequest(string playerName)
        {
            using (SQLiteConnection con = new SQLiteConnection(connectionString))
            {
                con.Open();
                // remove request
                // query
                string query = "DELETE FROM PendingFriendRequests WHERE receiverID = @receiverID AND senderID=@playerID";
                using (SQLiteCommand command = new SQLiteCommand(query, con))
                {
                    // Add the parameter and its value
                    command.Parameters.AddWithValue("@receiverID", playerName);
                    command.Parameters.AddWithValue("@playerID", userProfile.id);

                    // Execute the command
                    int rowsAffected = command.ExecuteNonQuery();
                    fetchFriendsList(false);

                    return true;
                }
            }
        }

        private void contextMenuStrip1_ItemClicked(object sender, ToolStripItemClickedEventArgs e)
        {
            int columnIndex = 0; // friendid

            // Check if the row index is valid
            if (rowIndex >= 0 && rowIndex < sentRequestsGridView.Rows.Count)
            {
                // Access the row at the specified index
                DataGridViewRow row = sentRequestsGridView.Rows[rowIndex];

                // Check if the column index is valid
                if (columnIndex >= 0 && columnIndex < row.Cells.Count)
                {
                    // Access the cell at the specified column index
                    DataGridViewCell cell = row.Cells[columnIndex];

                    // Retrieve the value of the cell
                    object cellValue = cell.Value;
                    string friendName = (string)cellValue;
                    switch (e.ClickedItem.Text)
                    {
                        case "Remove request":
                            removeSentFriendRequest(friendName);
                            break;

                        default:
                            break;
                    }



                }
            }


        }
    }
}
