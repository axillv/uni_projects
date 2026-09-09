using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FitQuest
{
    internal class FriendEntry
    {
        private string friendID;

        public String FriendID
        {
            get { return friendID; }
            set { friendID = value; }
        }


        public FriendEntry(string friendID)
        {
            this.friendID = friendID;
        }

        // public override string ToString() 

    }
}
