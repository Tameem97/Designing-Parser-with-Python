class Point3D extends Point {
      def constructor(x, y, z) {
        super(x, y);
        this.z = z;
      }
      def calc() {
        return super() + this.z;
      }
    }


let p =new Point3D(10, 20, 30);
p.calc();