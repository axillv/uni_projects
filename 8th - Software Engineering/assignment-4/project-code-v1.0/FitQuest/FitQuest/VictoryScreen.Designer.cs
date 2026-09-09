namespace FitQuest
{
    partial class VictoryScreen
    {
        /// <summary> 
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(VictoryScreen));
            this.label1 = new System.Windows.Forms.Label();
            this.GoldValueLabel = new System.Windows.Forms.Label();
            this.itemsListLabel = new System.Windows.Forms.Label();
            this.enemyNameVictoryLabel = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.itemsTitleLabel = new System.Windows.Forms.Label();
            this.btnGoBack = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Papyrus", 20.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.Color.White;
            this.label1.Location = new System.Drawing.Point(128, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(112, 42);
            this.label1.TabIndex = 0;
            this.label1.Text = "Victory!";
            // 
            // GoldValueLabel
            // 
            this.GoldValueLabel.AutoSize = true;
            this.GoldValueLabel.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.GoldValueLabel.ForeColor = System.Drawing.Color.White;
            this.GoldValueLabel.Location = new System.Drawing.Point(98, 184);
            this.GoldValueLabel.Name = "GoldValueLabel";
            this.GoldValueLabel.Size = new System.Drawing.Size(68, 33);
            this.GoldValueLabel.TabIndex = 2;
            this.GoldValueLabel.Text = "label3";
            // 
            // itemsListLabel
            // 
            this.itemsListLabel.AutoSize = true;
            this.itemsListLabel.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.itemsListLabel.ForeColor = System.Drawing.Color.White;
            this.itemsListLabel.Location = new System.Drawing.Point(238, 183);
            this.itemsListLabel.Name = "itemsListLabel";
            this.itemsListLabel.Size = new System.Drawing.Size(68, 33);
            this.itemsListLabel.TabIndex = 18;
            this.itemsListLabel.Text = "label3";
            // 
            // enemyNameVictoryLabel
            // 
            this.enemyNameVictoryLabel.AutoSize = true;
            this.enemyNameVictoryLabel.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.enemyNameVictoryLabel.ForeColor = System.Drawing.Color.White;
            this.enemyNameVictoryLabel.Location = new System.Drawing.Point(77, 65);
            this.enemyNameVictoryLabel.Name = "enemyNameVictoryLabel";
            this.enemyNameVictoryLabel.Size = new System.Drawing.Size(188, 33);
            this.enemyNameVictoryLabel.TabIndex = 19;
            this.enemyNameVictoryLabel.Text = "You have defeated ";
            // 
            // label2
            // 
            this.label2.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.ForeColor = System.Drawing.Color.White;
            this.label2.Image = global::FitQuest.Properties.Resources.coins;
            this.label2.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.label2.Location = new System.Drawing.Point(77, 150);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(105, 33);
            this.label2.TabIndex = 21;
            this.label2.Text = "Gold";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // itemsTitleLabel
            // 
            this.itemsTitleLabel.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.itemsTitleLabel.ForeColor = System.Drawing.Color.White;
            this.itemsTitleLabel.Image = global::FitQuest.Properties.Resources.sword;
            this.itemsTitleLabel.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.itemsTitleLabel.Location = new System.Drawing.Point(214, 150);
            this.itemsTitleLabel.Name = "itemsTitleLabel";
            this.itemsTitleLabel.Size = new System.Drawing.Size(105, 33);
            this.itemsTitleLabel.TabIndex = 17;
            this.itemsTitleLabel.Text = "Items";
            this.itemsTitleLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // btnGoBack
            // 
            this.btnGoBack.BackColor = System.Drawing.Color.Transparent;
            this.btnGoBack.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.btnGoBack.FlatAppearance.BorderSize = 0;
            this.btnGoBack.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(161)));
            this.btnGoBack.ForeColor = System.Drawing.Color.Black;
            this.btnGoBack.Image = ((System.Drawing.Image)(resources.GetObject("btnGoBack.Image")));
            this.btnGoBack.Location = new System.Drawing.Point(3, 497);
            this.btnGoBack.Name = "btnGoBack";
            this.btnGoBack.Size = new System.Drawing.Size(113, 50);
            this.btnGoBack.TabIndex = 16;
            this.btnGoBack.Text = "Exit";
            this.btnGoBack.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            this.btnGoBack.UseVisualStyleBackColor = false;
            this.btnGoBack.Click += new System.EventHandler(this.btnGoBack_Click);
            // 
            // VictoryScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.Transparent;
            this.Controls.Add(this.label2);
            this.Controls.Add(this.enemyNameVictoryLabel);
            this.Controls.Add(this.itemsListLabel);
            this.Controls.Add(this.itemsTitleLabel);
            this.Controls.Add(this.btnGoBack);
            this.Controls.Add(this.GoldValueLabel);
            this.Controls.Add(this.label1);
            this.Name = "VictoryScreen";
            this.Size = new System.Drawing.Size(979, 591);
            this.Load += new System.EventHandler(this.VictoryScreen_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label GoldValueLabel;
        private System.Windows.Forms.Button btnGoBack;
        private System.Windows.Forms.Label itemsTitleLabel;
        private System.Windows.Forms.Label itemsListLabel;
        private System.Windows.Forms.Label enemyNameVictoryLabel;
        private System.Windows.Forms.Label label2;
    }
}
