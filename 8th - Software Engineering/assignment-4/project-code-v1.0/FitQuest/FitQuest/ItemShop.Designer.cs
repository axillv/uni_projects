namespace FitQuest
{
    partial class ItemShop
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(ItemShop));
            this.clantablabel = new System.Windows.Forms.Label();
            this.backButton = new System.Windows.Forms.Button();
            this.itemsList = new System.Windows.Forms.ListView();
            this.purchaseButton = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.attributeColumn = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.valueColumn = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.itemAttributes = new System.Windows.Forms.ListView();
            this.label2 = new System.Windows.Forms.Label();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // clantablabel
            // 
            this.clantablabel.AutoSize = true;
            this.clantablabel.BackColor = System.Drawing.Color.Transparent;
            this.clantablabel.Font = new System.Drawing.Font("Papyrus", 35.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.clantablabel.Location = new System.Drawing.Point(514, 6);
            this.clantablabel.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.clantablabel.Name = "clantablabel";
            this.clantablabel.Size = new System.Drawing.Size(374, 112);
            this.clantablabel.TabIndex = 2;
            this.clantablabel.Text = "Item Shop";
            // 
            // backButton
            // 
            this.backButton.BackColor = System.Drawing.Color.Transparent;
            this.backButton.Font = new System.Drawing.Font("Microsoft Sans Serif", 13.25F);
            this.backButton.ForeColor = System.Drawing.Color.Transparent;
            this.backButton.Image = global::FitQuest.Properties.Resources.btnGoBack_Image;
            this.backButton.Location = new System.Drawing.Point(45, 29);
            this.backButton.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.backButton.Name = "backButton";
            this.backButton.RightToLeft = System.Windows.Forms.RightToLeft.Yes;
            this.backButton.Size = new System.Drawing.Size(189, 83);
            this.backButton.TabIndex = 3;
            this.backButton.UseVisualStyleBackColor = false;
            this.backButton.Click += new System.EventHandler(this.backButton_Click);
            // 
            // itemsList
            // 
            this.itemsList.HideSelection = false;
            this.itemsList.Location = new System.Drawing.Point(312, 98);
            this.itemsList.Name = "itemsList";
            this.itemsList.OwnerDraw = true;
            this.itemsList.ShowItemToolTips = true;
            this.itemsList.Size = new System.Drawing.Size(786, 602);
            this.itemsList.TabIndex = 4;
            this.itemsList.UseCompatibleStateImageBehavior = false;
            this.itemsList.SelectedIndexChanged += new System.EventHandler(this.itemsList_SelectedIndexChanged);
            // 
            // purchaseButton
            // 
            this.purchaseButton.BackColor = System.Drawing.Color.LimeGreen;
            this.purchaseButton.Font = new System.Drawing.Font("Segoe UI Semibold", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(161)));
            this.purchaseButton.Location = new System.Drawing.Point(1244, 678);
            this.purchaseButton.Name = "purchaseButton";
            this.purchaseButton.Size = new System.Drawing.Size(159, 112);
            this.purchaseButton.TabIndex = 6;
            this.purchaseButton.Text = "PURCHASE";
            this.purchaseButton.UseVisualStyleBackColor = false;
            this.purchaseButton.Click += new System.EventHandler(this.purchaseButton_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.BackColor = System.Drawing.Color.Transparent;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 24F);
            this.label1.Location = new System.Drawing.Point(1161, 238);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(239, 55);
            this.label1.TabIndex = 8;
            this.label1.Text = "Item Stats";
            // 
            // attributeColumn
            // 
            this.attributeColumn.Text = "Attribute";
            this.attributeColumn.Width = 150;
            // 
            // valueColumn
            // 
            this.valueColumn.Text = "Value";
            this.valueColumn.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // itemAttributes
            // 
            this.itemAttributes.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.attributeColumn,
            this.valueColumn});
            this.itemAttributes.HideSelection = false;
            this.itemAttributes.Location = new System.Drawing.Point(1156, 310);
            this.itemAttributes.Name = "itemAttributes";
            this.itemAttributes.Size = new System.Drawing.Size(248, 252);
            this.itemAttributes.TabIndex = 7;
            this.itemAttributes.UseCompatibleStateImageBehavior = false;
            this.itemAttributes.View = System.Windows.Forms.View.Details;
            this.itemAttributes.SelectedIndexChanged += new System.EventHandler(this.itemAttributes_SelectedIndexChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12.25F);
            this.label2.Location = new System.Drawing.Point(1150, 588);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(145, 29);
            this.label2.TabIndex = 10;
            this.label2.Text = "Gold Value:";
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(1156, 623);
            this.textBox1.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.textBox1.Name = "textBox1";
            this.textBox1.ReadOnly = true;
            this.textBox1.Size = new System.Drawing.Size(244, 26);
            this.textBox1.TabIndex = 11;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = global::FitQuest.Properties.Resources.placeholder;
            this.pictureBox1.Location = new System.Drawing.Point(1198, 56);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(170, 160);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBox1.TabIndex = 9;
            this.pictureBox1.TabStop = false;
            // 
            // ItemShop
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(224)))), ((int)(((byte)(192)))));
            this.BackgroundImage = global::FitQuest.Properties.Resources.itemshop;
            this.ClientSize = new System.Drawing.Size(1444, 849);
            this.Controls.Add(this.textBox1);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.itemAttributes);
            this.Controls.Add(this.purchaseButton);
            this.Controls.Add(this.itemsList);
            this.Controls.Add(this.backButton);
            this.Controls.Add(this.clantablabel);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.Name = "ItemShop";
            this.Text = "FitQuest";
            this.Load += new System.EventHandler(this.ItemShop_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label clantablabel;
        private System.Windows.Forms.Button backButton;
        private System.Windows.Forms.ListView itemsList;
        private System.Windows.Forms.Button purchaseButton;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.ColumnHeader attributeColumn;
        private System.Windows.Forms.ColumnHeader valueColumn;
        private System.Windows.Forms.ListView itemAttributes;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox textBox1;
    }
}