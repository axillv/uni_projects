namespace FitQuest
{
    partial class CombatSystem
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

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(CombatSystem));
            this.combatTimer = new System.Windows.Forms.Timer(this.components);
            this.enemyHealthBar = new System.Windows.Forms.ProgressBar();
            this.inventoryButton = new System.Windows.Forms.Button();
            this.attackButton = new System.Windows.Forms.Button();
            this.fleeButton = new System.Windows.Forms.Button();
            this.healthBarLabel = new System.Windows.Forms.Label();
            this.enemyNameLabel = new System.Windows.Forms.Label();
            this.nodeInfo = new System.Windows.Forms.Label();
            this.secondsPassedLabel = new System.Windows.Forms.Label();
            this.timeCounterGroupBox = new System.Windows.Forms.GroupBox();
            this.exerciseDataGrid = new System.Windows.Forms.DataGridView();
            this.inactivityTimer = new System.Windows.Forms.Timer(this.components);
            this.afkCheckGroupBox = new System.Windows.Forms.GroupBox();
            this.afkCheckButton = new System.Windows.Forms.Button();
            this.afkCheckLabel = new System.Windows.Forms.Label();
            this.playerCharacterPictureBox = new System.Windows.Forms.PictureBox();
            this.enemyPictureBox = new System.Windows.Forms.PictureBox();
            this.characterInfoLabel = new System.Windows.Forms.Label();
            this.timeCounterGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.exerciseDataGrid)).BeginInit();
            this.afkCheckGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.playerCharacterPictureBox)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.enemyPictureBox)).BeginInit();
            this.SuspendLayout();
            // 
            // combatTimer
            // 
            this.combatTimer.Tick += new System.EventHandler(this.combatTimer_Tick);
            // 
            // enemyHealthBar
            // 
            this.enemyHealthBar.Location = new System.Drawing.Point(691, 94);
            this.enemyHealthBar.Name = "enemyHealthBar";
            this.enemyHealthBar.Size = new System.Drawing.Size(261, 23);
            this.enemyHealthBar.Style = System.Windows.Forms.ProgressBarStyle.Continuous;
            this.enemyHealthBar.TabIndex = 1;
            // 
            // inventoryButton
            // 
            this.inventoryButton.BackColor = System.Drawing.Color.Transparent;
            this.inventoryButton.BackgroundImage = global::FitQuest.Properties.Resources.button;
            this.inventoryButton.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.inventoryButton.FlatAppearance.BorderSize = 0;
            this.inventoryButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.inventoryButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.inventoryButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.inventoryButton.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.inventoryButton.Location = new System.Drawing.Point(4, 474);
            this.inventoryButton.Name = "inventoryButton";
            this.inventoryButton.Size = new System.Drawing.Size(154, 54);
            this.inventoryButton.TabIndex = 2;
            this.inventoryButton.Text = "Inventory";
            this.inventoryButton.UseVisualStyleBackColor = false;
            this.inventoryButton.Click += new System.EventHandler(this.inventoryButton_Click);
            // 
            // attackButton
            // 
            this.attackButton.BackColor = System.Drawing.Color.Transparent;
            this.attackButton.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("attackButton.BackgroundImage")));
            this.attackButton.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.attackButton.FlatAppearance.BorderSize = 0;
            this.attackButton.FlatAppearance.CheckedBackColor = System.Drawing.Color.Transparent;
            this.attackButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.attackButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.attackButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.attackButton.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.attackButton.Location = new System.Drawing.Point(164, 474);
            this.attackButton.Name = "attackButton";
            this.attackButton.Size = new System.Drawing.Size(154, 54);
            this.attackButton.TabIndex = 3;
            this.attackButton.Text = "Repetition";
            this.attackButton.UseVisualStyleBackColor = false;
            this.attackButton.Click += new System.EventHandler(this.attackButton_Click);
            // 
            // fleeButton
            // 
            this.fleeButton.BackColor = System.Drawing.Color.Transparent;
            this.fleeButton.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("fleeButton.BackgroundImage")));
            this.fleeButton.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.fleeButton.FlatAppearance.BorderSize = 0;
            this.fleeButton.FlatAppearance.CheckedBackColor = System.Drawing.Color.Transparent;
            this.fleeButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.fleeButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.fleeButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.fleeButton.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.fleeButton.Location = new System.Drawing.Point(324, 474);
            this.fleeButton.Name = "fleeButton";
            this.fleeButton.Size = new System.Drawing.Size(154, 54);
            this.fleeButton.TabIndex = 4;
            this.fleeButton.Text = "Flee combat";
            this.fleeButton.UseVisualStyleBackColor = false;
            this.fleeButton.Click += new System.EventHandler(this.fleeButton_Click);
            // 
            // healthBarLabel
            // 
            this.healthBarLabel.AutoSize = true;
            this.healthBarLabel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(192)))), ((int)(((byte)(255)))), ((int)(((byte)(192)))));
            this.healthBarLabel.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.healthBarLabel.Font = new System.Drawing.Font("Papyrus", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.healthBarLabel.ForeColor = System.Drawing.Color.Black;
            this.healthBarLabel.Location = new System.Drawing.Point(800, 93);
            this.healthBarLabel.Name = "healthBarLabel";
            this.healthBarLabel.Size = new System.Drawing.Size(49, 24);
            this.healthBarLabel.TabIndex = 5;
            this.healthBarLabel.Text = "label1";
            // 
            // enemyNameLabel
            // 
            this.enemyNameLabel.AutoSize = true;
            this.enemyNameLabel.BackColor = System.Drawing.Color.Transparent;
            this.enemyNameLabel.Font = new System.Drawing.Font("Papyrus", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.enemyNameLabel.ForeColor = System.Drawing.Color.White;
            this.enemyNameLabel.Location = new System.Drawing.Point(799, 66);
            this.enemyNameLabel.Name = "enemyNameLabel";
            this.enemyNameLabel.Size = new System.Drawing.Size(53, 25);
            this.enemyNameLabel.TabIndex = 7;
            this.enemyNameLabel.Text = "label1";
            // 
            // nodeInfo
            // 
            this.nodeInfo.AutoSize = true;
            this.nodeInfo.BackColor = System.Drawing.Color.Transparent;
            this.nodeInfo.Font = new System.Drawing.Font("Papyrus", 13.25F);
            this.nodeInfo.ForeColor = System.Drawing.Color.White;
            this.nodeInfo.Location = new System.Drawing.Point(447, 14);
            this.nodeInfo.Name = "nodeInfo";
            this.nodeInfo.Size = new System.Drawing.Size(57, 28);
            this.nodeInfo.TabIndex = 8;
            this.nodeInfo.Text = "label1";
            // 
            // secondsPassedLabel
            // 
            this.secondsPassedLabel.AutoSize = true;
            this.secondsPassedLabel.ForeColor = System.Drawing.Color.Black;
            this.secondsPassedLabel.Location = new System.Drawing.Point(6, 16);
            this.secondsPassedLabel.Name = "secondsPassedLabel";
            this.secondsPassedLabel.Size = new System.Drawing.Size(49, 24);
            this.secondsPassedLabel.TabIndex = 9;
            this.secondsPassedLabel.Text = "label1";
            // 
            // timeCounterGroupBox
            // 
            this.timeCounterGroupBox.BackColor = System.Drawing.Color.LightGray;
            this.timeCounterGroupBox.Controls.Add(this.secondsPassedLabel);
            this.timeCounterGroupBox.Font = new System.Drawing.Font("Papyrus", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.timeCounterGroupBox.Location = new System.Drawing.Point(30, 12);
            this.timeCounterGroupBox.Name = "timeCounterGroupBox";
            this.timeCounterGroupBox.Size = new System.Drawing.Size(200, 35);
            this.timeCounterGroupBox.TabIndex = 10;
            this.timeCounterGroupBox.TabStop = false;
            this.timeCounterGroupBox.Text = "Time";
            // 
            // exerciseDataGrid
            // 
            this.exerciseDataGrid.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.exerciseDataGrid.Location = new System.Drawing.Point(291, 45);
            this.exerciseDataGrid.Name = "exerciseDataGrid";
            this.exerciseDataGrid.ReadOnly = true;
            this.exerciseDataGrid.Size = new System.Drawing.Size(358, 150);
            this.exerciseDataGrid.TabIndex = 11;
            // 
            // inactivityTimer
            // 
            this.inactivityTimer.Tick += new System.EventHandler(this.inactivityTimer_Tick);
            // 
            // afkCheckGroupBox
            // 
            this.afkCheckGroupBox.BackColor = System.Drawing.Color.IndianRed;
            this.afkCheckGroupBox.Controls.Add(this.afkCheckButton);
            this.afkCheckGroupBox.Controls.Add(this.afkCheckLabel);
            this.afkCheckGroupBox.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.afkCheckGroupBox.ForeColor = System.Drawing.SystemColors.ControlText;
            this.afkCheckGroupBox.Location = new System.Drawing.Point(411, 300);
            this.afkCheckGroupBox.Name = "afkCheckGroupBox";
            this.afkCheckGroupBox.Size = new System.Drawing.Size(135, 83);
            this.afkCheckGroupBox.TabIndex = 12;
            this.afkCheckGroupBox.TabStop = false;
            this.afkCheckGroupBox.Visible = false;
            // 
            // afkCheckButton
            // 
            this.afkCheckButton.BackColor = System.Drawing.Color.Transparent;
            this.afkCheckButton.BackgroundImage = global::FitQuest.Properties.Resources.button;
            this.afkCheckButton.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.afkCheckButton.FlatAppearance.BorderSize = 0;
            this.afkCheckButton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.afkCheckButton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.afkCheckButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.afkCheckButton.Font = new System.Drawing.Font("Papyrus", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.afkCheckButton.Location = new System.Drawing.Point(20, 30);
            this.afkCheckButton.Name = "afkCheckButton";
            this.afkCheckButton.Size = new System.Drawing.Size(96, 48);
            this.afkCheckButton.TabIndex = 1;
            this.afkCheckButton.Text = "I\'m here!";
            this.afkCheckButton.UseVisualStyleBackColor = false;
            this.afkCheckButton.Click += new System.EventHandler(this.afkCheckButton_Click);
            // 
            // afkCheckLabel
            // 
            this.afkCheckLabel.AutoSize = true;
            this.afkCheckLabel.Font = new System.Drawing.Font("Papyrus", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.afkCheckLabel.Location = new System.Drawing.Point(9, 7);
            this.afkCheckLabel.Name = "afkCheckLabel";
            this.afkCheckLabel.Size = new System.Drawing.Size(118, 25);
            this.afkCheckLabel.TabIndex = 0;
            this.afkCheckLabel.Text = "Hey! Still here?";
            // 
            // playerCharacterPictureBox
            // 
            this.playerCharacterPictureBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(192)))), ((int)(((byte)(128)))));
            this.playerCharacterPictureBox.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("playerCharacterPictureBox.BackgroundImage")));
            this.playerCharacterPictureBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.playerCharacterPictureBox.Location = new System.Drawing.Point(30, 153);
            this.playerCharacterPictureBox.Name = "playerCharacterPictureBox";
            this.playerCharacterPictureBox.Size = new System.Drawing.Size(182, 314);
            this.playerCharacterPictureBox.TabIndex = 6;
            this.playerCharacterPictureBox.TabStop = false;
            // 
            // enemyPictureBox
            // 
            this.enemyPictureBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(192)))), ((int)(((byte)(128)))));
            this.enemyPictureBox.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("enemyPictureBox.BackgroundImage")));
            this.enemyPictureBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.enemyPictureBox.Location = new System.Drawing.Point(720, 123);
            this.enemyPictureBox.Name = "enemyPictureBox";
            this.enemyPictureBox.Size = new System.Drawing.Size(203, 355);
            this.enemyPictureBox.TabIndex = 0;
            this.enemyPictureBox.TabStop = false;
            // 
            // characterInfoLabel
            // 
            this.characterInfoLabel.AutoSize = true;
            this.characterInfoLabel.BackColor = System.Drawing.Color.Transparent;
            this.characterInfoLabel.Font = new System.Drawing.Font("Papyrus", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.characterInfoLabel.ForeColor = System.Drawing.Color.White;
            this.characterInfoLabel.Location = new System.Drawing.Point(81, 123);
            this.characterInfoLabel.Name = "characterInfoLabel";
            this.characterInfoLabel.Size = new System.Drawing.Size(53, 25);
            this.characterInfoLabel.TabIndex = 13;
            this.characterInfoLabel.Text = "label1";
            // 
            // CombatSystem
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.BackgroundImage = global::FitQuest.Properties.Resources.autumn_forest_acrylic_painting_spooky_mystery_dusk_generated_by_ai;
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.ClientSize = new System.Drawing.Size(963, 552);
            this.Controls.Add(this.characterInfoLabel);
            this.Controls.Add(this.afkCheckGroupBox);
            this.Controls.Add(this.exerciseDataGrid);
            this.Controls.Add(this.timeCounterGroupBox);
            this.Controls.Add(this.nodeInfo);
            this.Controls.Add(this.enemyNameLabel);
            this.Controls.Add(this.playerCharacterPictureBox);
            this.Controls.Add(this.healthBarLabel);
            this.Controls.Add(this.fleeButton);
            this.Controls.Add(this.attackButton);
            this.Controls.Add(this.inventoryButton);
            this.Controls.Add(this.enemyHealthBar);
            this.Controls.Add(this.enemyPictureBox);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "CombatSystem";
            this.Text = "FitQuest";
            this.Load += new System.EventHandler(this.CombatSystem_Load);
            this.timeCounterGroupBox.ResumeLayout(false);
            this.timeCounterGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.exerciseDataGrid)).EndInit();
            this.afkCheckGroupBox.ResumeLayout(false);
            this.afkCheckGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.playerCharacterPictureBox)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.enemyPictureBox)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Timer combatTimer;
        private System.Windows.Forms.PictureBox enemyPictureBox;
        private System.Windows.Forms.ProgressBar enemyHealthBar;
        private System.Windows.Forms.Button inventoryButton;
        private System.Windows.Forms.Button attackButton;
        private System.Windows.Forms.Button fleeButton;
        private System.Windows.Forms.Label healthBarLabel;
        private System.Windows.Forms.PictureBox playerCharacterPictureBox;
        private System.Windows.Forms.Label enemyNameLabel;
        private System.Windows.Forms.Label nodeInfo;
        private System.Windows.Forms.Label secondsPassedLabel;
        private System.Windows.Forms.GroupBox timeCounterGroupBox;
        private System.Windows.Forms.DataGridView exerciseDataGrid;
        private System.Windows.Forms.Timer inactivityTimer;
        private System.Windows.Forms.GroupBox afkCheckGroupBox;
        private System.Windows.Forms.Button afkCheckButton;
        private System.Windows.Forms.Label afkCheckLabel;
        private System.Windows.Forms.Label characterInfoLabel;
    }
}