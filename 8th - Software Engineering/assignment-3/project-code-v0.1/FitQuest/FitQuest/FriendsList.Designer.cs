namespace FitQuest
{
    partial class FriendsList
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
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle1 = new System.Windows.Forms.DataGridViewCellStyle();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FriendsList));
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle2 = new System.Windows.Forms.DataGridViewCellStyle();
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle3 = new System.Windows.Forms.DataGridViewCellStyle();
            this.dataGridView1 = new System.Windows.Forms.DataGridView();
            this.friendsTabMenuStrip = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.inviteToClanToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.removeFriendToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.lblNamePrompt = new System.Windows.Forms.Label();
            this.txtFriendName = new System.Windows.Forms.TextBox();
            this.btnSendRequest = new System.Windows.Forms.Button();
            this.lblResult = new System.Windows.Forms.Label();
            this.AddFriend = new System.Windows.Forms.Button();
            this.FriendsTab = new System.Windows.Forms.TabControl();
            this.FriendsTabPage = new System.Windows.Forms.TabPage();
            this.PendingRequestsTabPage = new System.Windows.Forms.TabPage();
            this.dataGridView2 = new System.Windows.Forms.DataGridView();
            this.friendRequestsMenuStrip = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.acceptFriendRequestToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.declineFriendRequestToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.lblfriendLink = new System.Windows.Forms.Label();
            this.txtfriendLink = new System.Windows.Forms.TextBox();
            this.sqLiteCommandBuilder1 = new System.Data.SQLite.SQLiteCommandBuilder();
            this.buttonGenerateFriendLink = new System.Windows.Forms.Button();
            this.btnGoBack = new System.Windows.Forms.Button();
            this.SuccessFriendActionLabel = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).BeginInit();
            this.friendsTabMenuStrip.SuspendLayout();
            this.FriendsTab.SuspendLayout();
            this.FriendsTabPage.SuspendLayout();
            this.PendingRequestsTabPage.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView2)).BeginInit();
            this.friendRequestsMenuStrip.SuspendLayout();
            this.SuspendLayout();
            // 
            // dataGridView1
            // 
            this.dataGridView1.AllowUserToAddRows = false;
            this.dataGridView1.AllowUserToDeleteRows = false;
            this.dataGridView1.AllowUserToResizeColumns = false;
            this.dataGridView1.AllowUserToResizeRows = false;
            this.dataGridView1.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dataGridView1.BackgroundColor = System.Drawing.Color.White;
            this.dataGridView1.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.DisableResizing;
            this.dataGridView1.ContextMenuStrip = this.friendsTabMenuStrip;
            dataGridViewCellStyle1.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle1.BackColor = System.Drawing.Color.White;
            dataGridViewCellStyle1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(161)));
            dataGridViewCellStyle1.ForeColor = System.Drawing.SystemColors.ControlText;
            dataGridViewCellStyle1.SelectionBackColor = System.Drawing.Color.White;
            dataGridViewCellStyle1.SelectionForeColor = System.Drawing.Color.Black;
            dataGridViewCellStyle1.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
            this.dataGridView1.DefaultCellStyle = dataGridViewCellStyle1;
            this.dataGridView1.GridColor = System.Drawing.Color.White;
            this.dataGridView1.Location = new System.Drawing.Point(0, 0);
            this.dataGridView1.Name = "dataGridView1";
            this.dataGridView1.ReadOnly = true;
            this.dataGridView1.RowHeadersBorderStyle = System.Windows.Forms.DataGridViewHeaderBorderStyle.None;
            this.dataGridView1.RowHeadersVisible = false;
            this.dataGridView1.ShowEditingIcon = false;
            this.dataGridView1.Size = new System.Drawing.Size(398, 265);
            this.dataGridView1.TabIndex = 2;
            this.dataGridView1.CellContentClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView1_CellContentClick);
            this.dataGridView1.CellFormatting += new System.Windows.Forms.DataGridViewCellFormattingEventHandler(this.dataGridView1_CellFormatting);
            // 
            // friendsTabMenuStrip
            // 
            this.friendsTabMenuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.inviteToClanToolStripMenuItem,
            this.removeFriendToolStripMenuItem});
            this.friendsTabMenuStrip.Name = "friendsTabMenuStrip";
            this.friendsTabMenuStrip.ShowImageMargin = false;
            this.friendsTabMenuStrip.Size = new System.Drawing.Size(127, 48);
            this.friendsTabMenuStrip.Opening += new System.ComponentModel.CancelEventHandler(this.friendsTabMenuStrip_Opening);
            this.friendsTabMenuStrip.ItemClicked += new System.Windows.Forms.ToolStripItemClickedEventHandler(this.friendsTabMenuStrip_ItemClicked);
            // 
            // inviteToClanToolStripMenuItem
            // 
            this.inviteToClanToolStripMenuItem.Name = "inviteToClanToolStripMenuItem";
            this.inviteToClanToolStripMenuItem.Size = new System.Drawing.Size(126, 22);
            this.inviteToClanToolStripMenuItem.Text = "Invite to clan";
            // 
            // removeFriendToolStripMenuItem
            // 
            this.removeFriendToolStripMenuItem.Name = "removeFriendToolStripMenuItem";
            this.removeFriendToolStripMenuItem.Size = new System.Drawing.Size(126, 22);
            this.removeFriendToolStripMenuItem.Text = "Remove friend";
            // 
            // lblNamePrompt
            // 
            this.lblNamePrompt.AutoSize = true;
            this.lblNamePrompt.Location = new System.Drawing.Point(427, 41);
            this.lblNamePrompt.Name = "lblNamePrompt";
            this.lblNamePrompt.Size = new System.Drawing.Size(102, 13);
            this.lblNamePrompt.TabIndex = 4;
            this.lblNamePrompt.Text = "Enter Friend\'s Name";
            this.lblNamePrompt.Visible = false;
            // 
            // txtFriendName
            // 
            this.txtFriendName.Location = new System.Drawing.Point(562, 34);
            this.txtFriendName.Name = "txtFriendName";
            this.txtFriendName.Size = new System.Drawing.Size(198, 20);
            this.txtFriendName.TabIndex = 5;
            this.txtFriendName.Visible = false;
            // 
            // btnSendRequest
            // 
            this.btnSendRequest.Location = new System.Drawing.Point(766, 31);
            this.btnSendRequest.Name = "btnSendRequest";
            this.btnSendRequest.Size = new System.Drawing.Size(85, 24);
            this.btnSendRequest.TabIndex = 6;
            this.btnSendRequest.Text = "Send Request";
            this.btnSendRequest.UseVisualStyleBackColor = true;
            this.btnSendRequest.Visible = false;
            this.btnSendRequest.Click += new System.EventHandler(this.btnSendRequest_Click);
            // 
            // lblResult
            // 
            this.lblResult.AutoSize = true;
            this.lblResult.Location = new System.Drawing.Point(427, 60);
            this.lblResult.Name = "lblResult";
            this.lblResult.Size = new System.Drawing.Size(0, 13);
            this.lblResult.TabIndex = 7;
            this.lblResult.Visible = false;
            // 
            // AddFriend
            // 
            this.AddFriend.BackColor = System.Drawing.Color.Transparent;
            this.AddFriend.FlatAppearance.BorderSize = 0;
            this.AddFriend.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.AddFriend.Image = ((System.Drawing.Image)(resources.GetObject("AddFriend.Image")));
            this.AddFriend.Location = new System.Drawing.Point(424, 12);
            this.AddFriend.Name = "AddFriend";
            this.AddFriend.Size = new System.Drawing.Size(93, 24);
            this.AddFriend.TabIndex = 8;
            this.AddFriend.Text = " Add Friend";
            this.AddFriend.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            this.AddFriend.UseVisualStyleBackColor = false;
            this.AddFriend.Click += new System.EventHandler(this.AddFriend_Click);
            // 
            // FriendsTab
            // 
            this.FriendsTab.Controls.Add(this.FriendsTabPage);
            this.FriendsTab.Controls.Add(this.PendingRequestsTabPage);
            this.FriendsTab.Location = new System.Drawing.Point(12, 12);
            this.FriendsTab.Name = "FriendsTab";
            this.FriendsTab.SelectedIndex = 0;
            this.FriendsTab.Size = new System.Drawing.Size(406, 291);
            this.FriendsTab.TabIndex = 9;
            this.FriendsTab.SelectedIndexChanged += new System.EventHandler(this.FriendsTab_SelectedIndexChanged);
            // 
            // FriendsTabPage
            // 
            this.FriendsTabPage.Controls.Add(this.dataGridView1);
            this.FriendsTabPage.Location = new System.Drawing.Point(4, 22);
            this.FriendsTabPage.Name = "FriendsTabPage";
            this.FriendsTabPage.Padding = new System.Windows.Forms.Padding(3);
            this.FriendsTabPage.Size = new System.Drawing.Size(398, 265);
            this.FriendsTabPage.TabIndex = 0;
            this.FriendsTabPage.Text = "Friends list";
            this.FriendsTabPage.UseVisualStyleBackColor = true;
            this.FriendsTabPage.Click += new System.EventHandler(this.FriendsTab_Click);
            // 
            // PendingRequestsTabPage
            // 
            this.PendingRequestsTabPage.Controls.Add(this.dataGridView2);
            this.PendingRequestsTabPage.Location = new System.Drawing.Point(4, 22);
            this.PendingRequestsTabPage.Name = "PendingRequestsTabPage";
            this.PendingRequestsTabPage.Padding = new System.Windows.Forms.Padding(3);
            this.PendingRequestsTabPage.Size = new System.Drawing.Size(398, 265);
            this.PendingRequestsTabPage.TabIndex = 1;
            this.PendingRequestsTabPage.Text = "Pending requests";
            this.PendingRequestsTabPage.UseVisualStyleBackColor = true;
            // 
            // dataGridView2
            // 
            this.dataGridView2.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dataGridView2.BackgroundColor = System.Drawing.Color.White;
            this.dataGridView2.BorderStyle = System.Windows.Forms.BorderStyle.None;
            dataGridViewCellStyle2.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle2.BackColor = System.Drawing.Color.White;
            dataGridViewCellStyle2.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(161)));
            dataGridViewCellStyle2.ForeColor = System.Drawing.SystemColors.WindowText;
            dataGridViewCellStyle2.SelectionBackColor = System.Drawing.Color.White;
            dataGridViewCellStyle2.SelectionForeColor = System.Drawing.Color.Transparent;
            dataGridViewCellStyle2.WrapMode = System.Windows.Forms.DataGridViewTriState.True;
            this.dataGridView2.ColumnHeadersDefaultCellStyle = dataGridViewCellStyle2;
            this.dataGridView2.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView2.ContextMenuStrip = this.friendRequestsMenuStrip;
            dataGridViewCellStyle3.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle3.BackColor = System.Drawing.Color.White;
            dataGridViewCellStyle3.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(161)));
            dataGridViewCellStyle3.ForeColor = System.Drawing.SystemColors.ControlText;
            dataGridViewCellStyle3.SelectionBackColor = System.Drawing.Color.White;
            dataGridViewCellStyle3.SelectionForeColor = System.Drawing.Color.Black;
            dataGridViewCellStyle3.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
            this.dataGridView2.DefaultCellStyle = dataGridViewCellStyle3;
            this.dataGridView2.GridColor = System.Drawing.Color.White;
            this.dataGridView2.Location = new System.Drawing.Point(0, 0);
            this.dataGridView2.Name = "dataGridView2";
            this.dataGridView2.ReadOnly = true;
            this.dataGridView2.RowHeadersBorderStyle = System.Windows.Forms.DataGridViewHeaderBorderStyle.None;
            this.dataGridView2.RowHeadersVisible = false;
            this.dataGridView2.ShowEditingIcon = false;
            this.dataGridView2.Size = new System.Drawing.Size(398, 265);
            this.dataGridView2.TabIndex = 0;
            this.dataGridView2.CellContentClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView2_CellContentClick);
            // 
            // friendRequestsMenuStrip
            // 
            this.friendRequestsMenuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.acceptFriendRequestToolStripMenuItem,
            this.declineFriendRequestToolStripMenuItem});
            this.friendRequestsMenuStrip.Name = "friendRequestsMenuStrip";
            this.friendRequestsMenuStrip.Size = new System.Drawing.Size(190, 48);
            // 
            // acceptFriendRequestToolStripMenuItem
            // 
            this.acceptFriendRequestToolStripMenuItem.Name = "acceptFriendRequestToolStripMenuItem";
            this.acceptFriendRequestToolStripMenuItem.Size = new System.Drawing.Size(189, 22);
            this.acceptFriendRequestToolStripMenuItem.Text = "Accept friend request";
            // 
            // declineFriendRequestToolStripMenuItem
            // 
            this.declineFriendRequestToolStripMenuItem.Name = "declineFriendRequestToolStripMenuItem";
            this.declineFriendRequestToolStripMenuItem.Size = new System.Drawing.Size(189, 22);
            this.declineFriendRequestToolStripMenuItem.Text = "Decline friend request";
            // 
            // lblfriendLink
            // 
            this.lblfriendLink.AutoSize = true;
            this.lblfriendLink.Location = new System.Drawing.Point(427, 90);
            this.lblfriendLink.Name = "lblfriendLink";
            this.lblfriendLink.Size = new System.Drawing.Size(122, 13);
            this.lblfriendLink.TabIndex = 11;
            this.lblfriendLink.Text = "Generate friend invite url";
            this.lblfriendLink.Visible = false;
            this.lblfriendLink.Click += new System.EventHandler(this.lblfriendLink_Click);
            // 
            // txtfriendLink
            // 
            this.txtfriendLink.Location = new System.Drawing.Point(562, 83);
            this.txtfriendLink.Name = "txtfriendLink";
            this.txtfriendLink.ReadOnly = true;
            this.txtfriendLink.Size = new System.Drawing.Size(198, 20);
            this.txtfriendLink.TabIndex = 12;
            this.txtfriendLink.Visible = false;
            this.txtfriendLink.TextChanged += new System.EventHandler(this.txtfriendLink_TextChanged);
            // 
            // sqLiteCommandBuilder1
            // 
            this.sqLiteCommandBuilder1.DataAdapter = null;
            this.sqLiteCommandBuilder1.QuoteSuffix = "]";
            // 
            // buttonGenerateFriendLink
            // 
            this.buttonGenerateFriendLink.Location = new System.Drawing.Point(766, 80);
            this.buttonGenerateFriendLink.Name = "buttonGenerateFriendLink";
            this.buttonGenerateFriendLink.Size = new System.Drawing.Size(84, 24);
            this.buttonGenerateFriendLink.TabIndex = 13;
            this.buttonGenerateFriendLink.Text = "Generate Link";
            this.buttonGenerateFriendLink.UseVisualStyleBackColor = true;
            this.buttonGenerateFriendLink.Visible = false;
            this.buttonGenerateFriendLink.Click += new System.EventHandler(this.buttonGenerateFriendLink_Click);
            // 
            // btnGoBack
            // 
            this.btnGoBack.BackColor = System.Drawing.Color.Transparent;
            this.btnGoBack.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.btnGoBack.FlatAppearance.BorderSize = 0;
            this.btnGoBack.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnGoBack.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(161)));
            this.btnGoBack.Image = ((System.Drawing.Image)(resources.GetObject("btnGoBack.Image")));
            this.btnGoBack.Location = new System.Drawing.Point(12, 490);
            this.btnGoBack.Name = "btnGoBack";
            this.btnGoBack.Size = new System.Drawing.Size(178, 50);
            this.btnGoBack.TabIndex = 15;
            this.btnGoBack.Text = "Exit friends list";
            this.btnGoBack.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            this.btnGoBack.UseVisualStyleBackColor = false;
            this.btnGoBack.Click += new System.EventHandler(this.btnGoBack_Click);
            // 
            // SuccessFriendActionLabel
            // 
            this.SuccessFriendActionLabel.AutoSize = true;
            this.SuccessFriendActionLabel.Location = new System.Drawing.Point(13, 310);
            this.SuccessFriendActionLabel.Name = "SuccessFriendActionLabel";
            this.SuccessFriendActionLabel.Size = new System.Drawing.Size(35, 13);
            this.SuccessFriendActionLabel.TabIndex = 16;
            this.SuccessFriendActionLabel.Text = "label1";
            this.SuccessFriendActionLabel.Visible = false;
            // 
            // FriendsList
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(224)))), ((int)(((byte)(192)))));
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.ClientSize = new System.Drawing.Size(963, 552);
            this.Controls.Add(this.SuccessFriendActionLabel);
            this.Controls.Add(this.btnGoBack);
            this.Controls.Add(this.buttonGenerateFriendLink);
            this.Controls.Add(this.txtfriendLink);
            this.Controls.Add(this.lblfriendLink);
            this.Controls.Add(this.FriendsTab);
            this.Controls.Add(this.AddFriend);
            this.Controls.Add(this.lblResult);
            this.Controls.Add(this.btnSendRequest);
            this.Controls.Add(this.txtFriendName);
            this.Controls.Add(this.lblNamePrompt);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "FriendsList";
            this.Text = "FitQuest";
            this.Load += new System.EventHandler(this.FriendsList_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).EndInit();
            this.friendsTabMenuStrip.ResumeLayout(false);
            this.FriendsTab.ResumeLayout(false);
            this.FriendsTabPage.ResumeLayout(false);
            this.PendingRequestsTabPage.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView2)).EndInit();
            this.friendRequestsMenuStrip.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.DataGridView dataGridView1;
        private System.Windows.Forms.Label lblNamePrompt;
        private System.Windows.Forms.TextBox txtFriendName;
        private System.Windows.Forms.Button btnSendRequest;
        private System.Windows.Forms.Label lblResult;
        private System.Windows.Forms.Button AddFriend;
        private System.Windows.Forms.TabControl FriendsTab;
        private System.Windows.Forms.TabPage FriendsTabPage;
        private System.Windows.Forms.TabPage PendingRequestsTabPage;
        private System.Windows.Forms.DataGridView dataGridView2;
        private System.Windows.Forms.Label lblfriendLink;
        private System.Windows.Forms.TextBox txtfriendLink;
        private System.Data.SQLite.SQLiteCommandBuilder sqLiteCommandBuilder1;
        private System.Windows.Forms.Button buttonGenerateFriendLink;
        private System.Windows.Forms.ContextMenuStrip friendsTabMenuStrip;
        private System.Windows.Forms.ToolStripMenuItem inviteToClanToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem removeFriendToolStripMenuItem;
        private System.Windows.Forms.Button btnGoBack;
        private System.Windows.Forms.ContextMenuStrip friendRequestsMenuStrip;
        private System.Windows.Forms.ToolStripMenuItem acceptFriendRequestToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem declineFriendRequestToolStripMenuItem;
        private System.Windows.Forms.Label SuccessFriendActionLabel;
    }
}

