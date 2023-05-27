from varwizard import VarWizard

model = VarWizard(model_name = "bloom-560m")
code = """
public class Main {
    public static void main(String args[]) {

        String line = "This order was placed for QT3000! OK?";
        String pattern = "(.*)(\\d+)(.*)";

        Pattern r = Pattern.compile(pattern);
        Matcher m = r.matcher(line);
        if (m.find()) {
            System.out.println("Found value: " + m.group(0));
            System.out.println("Found value: " + m.group(1));
            System.out.println("Found value: " + m.group(2));
        } else {
            System.out.println("NO MATCH");
        }
    }
}"""

print(model.make_new_code(code, 'java', output_path = 'output.java'))