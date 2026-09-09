using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FitQuest
{
    public partial class MainPanel : Form
    {
        private Panel appPanel;
        public MainPanel()
        {
            InitializeComponent();

            // Initialize and configure the main panel
            appPanel = new Panel
            {
                Dock = DockStyle.Fill
            };
            this.Controls.Add(appPanel);

            // Initially load the first form
            ShowFormInPanel(new MainMenu());
        }


        private void ShowFormInPanel(Form form)
        {
            // Clear any existing controls in the panel
            appPanel.Controls.Clear();

            // Configure the form to be a child of the panel
            form.TopLevel = false;
            form.FormBorderStyle = FormBorderStyle.None;
            form.Dock = DockStyle.Fill;

            // Add the form to the panel's controls and show it
            appPanel.Controls.Add(form);
            form.Show();
        }

        private void MainPanel_Load(object sender, EventArgs e)
        {
            this.Controls.Add(new MainMenu());
        }
    }
}
