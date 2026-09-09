using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.XPath;

namespace FitQuest
{
    public class Rewards
    {
        private int currency;
        private List<Item> itemsList;

        public Rewards(int rewardPoints) 
        {
            // given rewardPoints, distribute rewards
            this.currency = 100;
        }

        public int getCurrency()
        {
            return this.currency;
        }
        public List<Item> getItemsList()
        {
            return this.itemsList;
        }

    }
}
