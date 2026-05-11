import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingConstants;

public class HelloWorld {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Yocto Java GUI");
        JLabel label = new JLabel("Hello Yocto Java GUI!", SwingConstants.CENTER);

        frame.add(label);

        frame.setSize(400, 200);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
