using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FitQuest
{
    internal class Repetition
    {
        // normalized 0 to 1 rating
        private float quality;
        private int fullDamage;


        public Repetition(int quality, int fullDamage)
        {
            this.quality = quality;
            this.fullDamage = fullDamage;
        }

        public int calculateDamage()
        {
            return (int) Math.Floor(quality * fullDamage);
        }

        public bool isDetected()
        {
            return true;
        }

    }
}
