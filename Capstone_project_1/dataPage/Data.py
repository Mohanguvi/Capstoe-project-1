
class PageSource:
    """
        To perform the testing for the OrangeHRM
        The test data are given from the DDF.xlsx Excel file.
       """

    def __init__(self):
        """
            The __init__() method initializes the class instance with the following attributes:
                - url: The URL of the web page.
                - LoginUrl: The URL of the login page.
                - excelFile: The path to an Excel file containing data.
                - sheetName: The name of the worksheet within the Excel file.
                - book: Loads the Excel file using the openpyxl library and assigns it to the book attribute.
                - file: Accesses the specific worksheet within the Excel file and assigns it to the file attribute.
        """
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        self.LoginUrl = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
        self.AddEmployee_Url = "https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee"
        self.editEmployee_Url = ("https://opensource-demo.orangehrmlive.com/web/index.php/pim/"
                                 "viewPersonalDetails/empNumber")
