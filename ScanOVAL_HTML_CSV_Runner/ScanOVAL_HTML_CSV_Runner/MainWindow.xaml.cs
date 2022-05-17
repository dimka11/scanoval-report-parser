using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace ScanOVAL_HTML_CSV_Runner
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
            System.Diagnostics.Process process = new System.Diagnostics.Process();
            //startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
            startInfo.UseShellExecute = false;
            startInfo.FileName = "python";
            startInfo.Arguments = $"{textBoxScriptPath.Text} {textBoxFolder.Text}";
            startInfo.WorkingDirectory = textBoxFolder.Text;
            process.StartInfo = startInfo;
            process.Start();
            //System.Diagnostics.Process.Start("python", $"{textBoxScriptPath.Text} {textBoxFolder.Text}");
        }

        private void dragDropArea_Drop(object sender, DragEventArgs e)
        {
            string[] files = (string[])e.Data.GetData(DataFormats.FileDrop);

            string last_file_name = "";
            foreach (var file in files)
            {
                var file_name = file.Replace(@"\", "/");
                last_file_name = file_name;
                listBox.Items.Add(file_name);
            }
            textBoxFolder.Text = last_file_name;
        }

        private void TextBox_Drop(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                string[] files = e.Data.GetData(DataFormats.FileDrop) as string[];
                if (files != null && files.Length > 0)
                {
                    ((TextBox)sender).Text = files[0];
                }
            }
        }

        private void TextBox_PreviewDragOver(object sender, DragEventArgs e)
        {
            e.Handled = true;
        }
    }
}
