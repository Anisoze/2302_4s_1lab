
class Entropy
{




    static void Main()
    {
        StreamReader sr = new StreamReader("in.txt");
        int n;
        n = int.Parse(sr.ReadLine());
        double[] p = new double[n] ;
        int R = 16808; //
        for (int i = 0 ; i < n ; i++)
        {
            double s = double.Parse(sr.ReadLine()); //
            p[i] = s/R;
            //p[i] = Double.Parse(sr.ReadLine());
            Console.WriteLine(p[i]);
        }
        double h=0.0;
        for (int i = 0 ;i < n ; i++)
        {
            h += p[i] * Math.Log2(p[i]);
        }
        Console.WriteLine("\n{0}",-h);
        StreamWriter sw = new StreamWriter("out.txt");
        sw.WriteLine(-h); 
        sw.Close();


    }
      
    
    
}
