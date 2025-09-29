import javax.swing.*;
import java.awt.*;

public class sudokuPanel extends JPanel {
    sudokuPanel() {
        JLabel[][] cells = new JLabel[9][9];
        this.setSize(400,300);
        this.setBackground(Color.white);
        this.setOpaque(true);
    }
   
}
