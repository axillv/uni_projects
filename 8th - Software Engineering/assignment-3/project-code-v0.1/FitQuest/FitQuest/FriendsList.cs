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
        string connectionString;
        bool hasInternetConnectionBool;
        public FriendsList()
        {
            this.connectionString = ConfigurationManager.ConnectionStrings["SQLiteDB"].ConnectionString;

            InitializeComponent();

            this.hasInternetConnectionBool = hasInternetConnection();


            // Attach the event handler to the Load event of the form
            this.Load += FriendsList_Load;
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
                    // query
                    string query = "SELECT * FROM Friends";
                    SQLiteCommand cmd = new SQLiteCommand(query, con);
                    // data
                    DataTable dt = new DataTable();
                    SQLiteDataAdapter adapter = new SQLiteDataAdapter(cmd);
                    adapter.Fill(dt);

                    dataGridView1.DataSource = dt;

                    // query
                    string query2 = "SELECT * FROM PendingFriendRequests";
                    SQLiteCommand cmd2 = new SQLiteCommand(query2, con);
                    // data
                    DataTable dt2 = new DataTable();
                    SQLiteDataAdapter adapter2 = new SQLiteDataAdapter(cmd2);
                    adapter2.Fill(dt2);

                    dataGridView2.DataSource = dt2;
                    dataGridView2.ColumnHeadersHeight = 23;

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
            else {

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

        private bool hasInternetConnection()
        {
            return true;
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
            MainMenu MenuForm= new MainMenu();
            MenuForm.Show();
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

        private bool inviteFriendToClan(string friendName)
        {
            return true;
        }

        private bool deleteFriend(string friendName)
        {
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


                default:
                    break;
            }
        }

        private void friendsTabMenuStrip_ItemClicked(object sender, ToolStripItemClickedEventArgs e)
        {
            Console.WriteLine(e.ClickedItem);

            switch(e.ClickedItem.Text)
            {
                case "Invite to clan":
                    // pass friendName from datagridview when clicked
                    inviteFriendToClan("friendName");
                    displayFriendActionSuccess("clan", "friendName");
                    break;

                case "Remove friend":
                    // pass friendName from datagridview when clicked
                    if (deleteFriend("friendName"))
                    {
                        fetchFriendsList(false);
                        displayFriendActionSuccess("delete", "friendName");
                    }
                    break;

                default:
                    break;
            }

        }

        private void FriendsTab_SelectedIndexChanged(object sender, EventArgs e)
        {
            // reset info label
            SuccessFriendActionLabel.Visible = false;
            SuccessFriendActionLabel.Text = "";
        }
    }
}
