"""
Author: Andrew DeCandia
Project: Air Partners

Functions to collect figures into a static report PDF
"""
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import img2pdf
import os


def generate_report(month, year, sn):
    generator = ReportGenerator(month, year, sn)
    generator.generate_report()

class ReportGenerator:

    def __init__(self, month, year, sn):
        self.month = month
        self.year = year
        self.sn = sn
        self.year_month = str(self.year) + '-0' + str(self.month) if self.month <= 9 else str(self.year) + '-' + str(self.month)

    def _create_report_image(self):
        """
        """

        def import_and_plot_img(plot_function):
            
            plt.grid(0);plt.yticks([]);plt.xticks([])
            img = mpimg.imread('{1}/Graphs/{2}/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, plot_function))
            plt.imshow(img)
        fig = plt.figure(figsize=(8.3,11.7))
        grid = plt.GridSpec(20, 6, wspace=0.3, hspace=10)
        graph_title_position = 0.98
        graph_title_size = 15

        ## Header
        fig.add_subplot(grid[:4,:])
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
        'This report has data collected from the community owned air sensor network in Roxbury in collaboration\n\
        with ACE. The sensors are QuantAQ ModulairTM PM and measure Particulate Matter (PM) from burning fossil\n\
        fuels that is harmful to human health. If you have any questions or concerns, please contact\n\
        <INSERT CONTACT INFO>.'
            ,fontsize=8, y=0.1)
        dic_month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
                    7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
        plt.suptitle('  {0} {1}: {2}'.format(dic_month[self.month], self.year, self.sn), fontsize=21, y=0.86)

        ## Timeplots with Thresholds
        fig.add_subplot(grid[4:10,:])
        plt.title('PM Over Time', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("timeplot_threshold")
        

        ## Calendar plot
        fig.add_subplot(grid[10:15,:3])
        plt.title('Calendar', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("calendar_plot")

        ## Time of day plot
        fig.add_subplot(grid[10:15,3:6])
        plt.title('Time of Day', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("time_of_day_plot")

        ## Daily average plot
        fig.add_subplot(grid[15:20,:3])
        plt.title('Daily Average', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("daily_average_plot")

        ## Polar plot
        fig.add_subplot(grid[15:20,3:6])
        plt.title('Polar Plot', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("wind_polar_plot")

        try:
            os.mkdir('{}/Reports'.format(year_month))
        except: # Forgive my crime here, but it just avoids errors if the directory already exists
            pass
        plt.savefig('{1}/Reports/{0}_{1}_{2}.jpeg'.format(self.sn,self.year_month,str('Report')), bbox_inches='tight',dpi = 300)

    def _create_report_pdf(self):
        """
        Makes a PDF copy of the jpeg version of the report.
        _create_report_image MUST be run first.        
        """

        def image_to_pdf(img_path, pdf_path):
            ImgFile = open(img_path,"rb")
            PdfFile = open(pdf_path,"wb")
            PdfFile.write(img2pdf.convert(ImgFile))
            ImgFile.close()
            PdfFile.close()

        try:
            os.mkdir('{}/Reports/PDFs'.format(self.year_month))
        except: # Forgive my crime here, but it just avoids errors if the directory already exists
            pass
        image_to_pdf('{1}/Reports/{0}_{1}_{2}.jpeg'.format(self.sn,self.year_month,str('Report')),
                    '{1}/Reports/PDFs/{0}_{1}_{2}.pdf'.format(self.sn,self.year_month,str('Report')))

    
    def generate_report(self):
        """
        Generate a JPEG and PDF report for a given month and year
        """
        self._create_report_image()
        self._create_report_pdf()


    


    