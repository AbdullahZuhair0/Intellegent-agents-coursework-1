import javax.swing.JFrame;
import java.awt.*;

public class GuiBase extends JFrame{
    private static sudokuPanel sPanel = new sudokuPanel();
    GuiBase() {
        GridBagConstraints con = new GridBagConstraints();
        
        this.setLayout(new GridLayout(3,3));
        this.setSize(1300,1000);
        this.setVisible(true);
        this.getContentPane().setBackground(Color.DARK_GRAY);
        this.add(sPanel);
    }
}
