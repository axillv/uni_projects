namespace FitQuest
{
    partial class DefeatScreen
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
            this.DefeatLabel = new System.Windows.Forms.Label();
            this.btnGoBack = new System.Windows.Forms.Button();
            this.defeatStuffLabel = new System.Windows.Forms.Label();
            this.enemyInfoDefeatLabel = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // DefeatLabel
            // 
            this.DefeatLabel.AutoSize = true;
            this.DefeatLabel.BackColor = System.Drawing.Color.Transparent;
            this.DefeatLabel.Font = new System.Drawing.Font("Papyrus", 20.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.DefeatLabel.ForeColor = System.Drawing.Color.Black;
            this.DefeatLabel.Location = new System.Drawing.Point(262, 24);
            this.DefeatLabel.Name = "DefeatLabel";
            this.DefeatLabel.Size = new System.Drawing.Size(337, 42);
            this.DefeatLabel.TabIndex = 0;
            this.DefeatLabel.Text = "You lost! But do not falter!";
            // 
            // btnGoBack
            // 
            this.btnGoBack.BackColor = System.Drawing.Color.Transparent;
            this.btnGoBack.BackgroundImage = global::FitQuest.Properties.Resources.btnGoBack_Image;
            this.btnGoBack.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.btnGoBack.FlatAppearance.BorderSize = 0;
            this.btnGoBack.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(161)));
            this.btnGoBack.Location = new System.Drawing.Point(3, 495);
            this.btnGoBack.Name = "btnGoBack";
            this.btnGoBack.Size = new System.Drawing.Size(108, 40);
            this.btnGoBack.TabIndex = 16;
            this.btnGoBack.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            this.btnGoBack.UseVisualStyleBackColor = false;
            this.btnGoBack.Click += new System.EventHandler(this.btnGoBack_Click);
            // 
            // defeatStuffLabel
            // 
            this.defeatStuffLabel.AutoSize = true;
            this.defeatStuffLabel.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.defeatStuffLabel.Location = new System.Drawing.Point(41, 86);
            this.defeatStuffLabel.Name = "defeatStuffLabel";
            this.defeatStuffLabel.Size = new System.Drawing.Size(402, 33);
            this.defeatStuffLabel.TabIndex = 18;
            this.defeatStuffLabel.Text = "You fought well but your enemy bested you!";
            // 
            // enemyInfoDefeatLabel
            // 
            this.enemyInfoDefeatLabel.AutoSize = true;
            this.enemyInfoDefeatLabel.Font = new System.Drawing.Font("Papyrus", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.enemyInfoDefeatLabel.Location = new System.Drawing.Point(41, 137);
            this.enemyInfoDefeatLabel.Name = "enemyInfoDefeatLabel";
            this.enemyInfoDefeatLabel.Size = new System.Drawing.Size(424, 33);
            this.enemyInfoDefeatLabel.TabIndex = 19;
            this.enemyInfoDefeatLabel.Text = "When you come back again the enemy will have ";
            // 
            // DefeatScreen
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.Transparent;
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.Controls.Add(this.enemyInfoDefeatLabel);
            this.Controls.Add(this.defeatStuffLabel);
            this.Controls.Add(this.btnGoBack);
            this.Controls.Add(this.DefeatLabel);
            this.Name = "DefeatScreen";
            this.Size = new System.Drawing.Size(979, 591);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label DefeatLabel;
        private System.Windows.Forms.Button btnGoBack;
        private System.Windows.Forms.Label defeatStuffLabel;
        private System.Windows.Forms.Label enemyInfoDefeatLabel;
    }
}
