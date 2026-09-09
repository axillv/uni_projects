using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FitQuest
{
    public class Item
    {
        private Hashtable stats = new Hashtable();
        private string name;
        private int value, quantity;
        public enum categories
        {
            Weapon = 0,
            Armour = 1,
            Accessory = 2,
            Consumable = 3
        };
        private categories category;

        public Item(string name, int value, int quantity, categories category)
        {
            this.name = name;
            this.value = value;
            this.quantity = quantity;
            this.category = category;
            stats.Add("Damage", 5); // Example stat, can be changed
        }

        public categories getCategory()
        {
            return this.category;
        }

        public Hashtable GetStats()
        {
            return this.stats;
        }
    }
}
