using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static FitQuest.Item;

namespace FitQuest
{
    public class ConsumableItemInstance
    {
        private Hashtable stats = new Hashtable();
        private string name;

        public ConsumableItemInstance(string name)
        {
            this.name = name;
            //stats.Add("Damage", 5); // Example stat, can be changed
        }

        public void addStats(string AttrName, int AttrValue)
        {
            stats.Add(AttrName, AttrValue);
        }

        public Hashtable GetStats()
        {
            return this.stats;
        }



    }
}
