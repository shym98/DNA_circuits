function check_correctness() {
    var input_logic = document.getElementById("circuit").value;
    var objShell = new ActiveXObject("Shell.Application");
    var command = "python C:\\Users\\shym9\\Documents\\GitHub\\DNA_circuits\\testDNA\\main.py -c " + input_logic;
    objShell.ShellExecute("cmd.exe", command);
}