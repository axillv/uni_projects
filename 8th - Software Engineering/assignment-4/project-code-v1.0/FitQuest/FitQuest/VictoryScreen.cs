using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.Header;

namespace FitQuest
{
    public partial class VictoryScreen : UserControl
    {
        public VictoryScreen(Rewards rewardsObj, string enemyName)
        {
            InitializeComponent();

            this.GoldValueLabel.Text = rewardsObj.getCurrency().ToString();
            this.itemsListLabel.Text = "";
            this.enemyNameVictoryLabel.Text += enemyName;
            if (rewardsObj.getItemsList() == null)
            {
                this.itemsListLabel.Text = "No items won!";
            }
            else
            {
                List<Item> itemsList = rewardsObj.getItemsList();
                if (itemsList.Count == 0) 
                {

                    this.itemsListLabel.Text = "No items won!";
                }
                else
                {
                    foreach (Item item in itemsList)
                    {
                        string itemString = "";
                        itemString += $"(Value: {item.getValue()}) {item.getName()}\n";
                        this.itemsListLabel.Text += itemString;
                    }
                }

            }
        }

        private void btnGoBack_Click(object sender, EventArgs e)
        {
            // Hide the current form (main menu)
            this.Hide();

            // Show the menu form
            MainMenu MenuForm = new MainMenu();
            MenuForm.Show();

            // close parent form
            this.Hide();
            this.FindForm().Close();
        }

        private void VictoryScreen_Load(object sender, EventArgs e)
        {

        }
    }
}
