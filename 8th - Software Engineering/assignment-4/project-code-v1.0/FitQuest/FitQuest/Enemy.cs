using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace FitQuest
{
    public class Enemy
    {
        public int currentHP;

        public int maxHP;

        public string EnemyName;

        public int level;

        // TODO: enemyIcon to select also the enemy png
        public Enemy(string name, int maxHP, int currentHP, int level) 
        {
            this.currentHP = currentHP;
            this.maxHP = maxHP;
            this.EnemyName = name;
        }

        public void takeDamage(int damage)
        {
            if (currentHP < damage)
            {
                currentHP = 0;
                return;
            }

            currentHP -= damage;
        }

        public bool isDead()
        {
            if (this.currentHP == 0)
            {
                return true;
            }

            return false;
        }

    }
}
