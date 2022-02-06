import java.lang.String;
import java.io.*;
import java.time.format.DateTimeFormatter;  
import java.time.LocalDateTime;
import java.util.Random;
import java.util.*;
import javax.swing.*;
import java.awt.event.*;  

public class chargen {
	/*
	JFrame f;  
	CharacterGenerator2(){  
	f=new JFrame();//creating instance of JFrame  
			  
	JButton b=new JButton("click");//creating instance of JButton  
	b.setBounds(130,100,100, 40);  
			  
	f.add(b);//adding button in JFrame  
			  
	f.setSize(400,500);//400 width and 500 height  
	f.setLayout(null);//using no layout managers  
	f.setVisible(true);//making the frame visible  
	}
	  */
public static void main(String[] args) throws IOException
{
	   JFrame f=new JFrame("Character Generator");
/*	   
    final JTextField tf=new JTextField();  
    tf.setBounds(50,50, 150,20);  
    JButton b=new JButton("Click Here");  
    b.setBounds(50,100,95,30); 	
    b.addActionListener(new ActionListener(){
public void actionPerformed(ActionEvent e){  
            tf.setText("Welcome to Javatpoint.");  
        }  
    });
	JButton scream=new JButton("Scream");
    scream.setBounds(50,150,95,30);
	scream.addActionListener(new ActionListener(){
	public void actionPerformed(ActionEvent e){  
            tf.setText("Reeeeee.");  
        }  
    }); 	
    f.add(b);f.add(tf);f.add(scream);
	*/
	int first_column_width = 200;
	JLabel outFileLabel = new JLabel("Output File Path");
	outFileLabel.setBounds(25,25,first_column_width,20);
	f.add(outFileLabel);
	final JTextField outFileField = new JTextField();
	outFileField.setBounds(25,50,first_column_width,20);
	f.add(outFileField);
	
	JLabel startLabel = new JLabel("Starting Number");
	startLabel.setBounds(25,75,first_column_width,20);
	f.add(startLabel);
	final JTextField startField = new JTextField();
	startField.setBounds(25,100,first_column_width,20);
	f.add(startField);
	
	JLabel idLabel = new JLabel("Starting ID");
	idLabel.setBounds(25,125,first_column_width,20);
	f.add(idLabel);
	final JTextField idField = new JTextField();
	idField.setBounds(25,150,first_column_width,20);
	f.add(idField);
	
	JLabel amountLabel = new JLabel("Amount to Generate");
	amountLabel.setBounds(25,175,first_column_width,20);
	f.add(amountLabel);
	final JTextField amountField = new JTextField();
	amountField.setBounds(25,200,first_column_width,20);
	f.add(amountField);
	
	JLabel maleNameLabel = new JLabel("Male Name List File Path");
	maleNameLabel.setBounds(25,225,first_column_width,20);
	f.add(maleNameLabel);
	final JTextField maleNameField = new JTextField();
	maleNameField.setBounds(25,250,first_column_width,20);
	f.add(maleNameField);
	
	JLabel femaleNameLabel = new JLabel("Female Name List File Path");
	femaleNameLabel.setBounds(25,275,first_column_width,20);
	f.add(femaleNameLabel);
	final JTextField femaleNameField = new JTextField();
	femaleNameField.setBounds(25,300,first_column_width,20);
	f.add(femaleNameField);
	
	JLabel religionLabel = new JLabel("Religion");
	religionLabel.setBounds(25,325,first_column_width,20);
	f.add(religionLabel);
	final JTextField religionTextField = new JTextField();
	religionTextField.setBounds(25,350,first_column_width,20);
	f.add(religionTextField);
	
	JLabel cultureLabel = new JLabel("Culture");
	cultureLabel.setBounds(25,375,first_column_width,20);
	f.add(cultureLabel);
	final JTextField cultureField = new JTextField();
	cultureField.setBounds(25,400,first_column_width,20);
	f.add(cultureField);
	
	JLabel dynastyLabel = new JLabel("Dynasty List File Path (Optional)");
	dynastyLabel.setBounds(25,425,first_column_width,20);
	f.add(dynastyLabel);
	final JTextField dynastyField = new JTextField();
	dynastyField.setBounds(25,450,first_column_width,20);
	f.add(dynastyField);
	
	JLabel femaleLabel = new JLabel("Female yes/no/random");
	femaleLabel.setBounds(25,475,first_column_width,20);
	f.add(femaleLabel);
	String[] femaleOptions = {"yes", "no", "random"};
	JComboBox femaleComboBox = new JComboBox(femaleOptions);
	femaleComboBox.setBounds(25,500,first_column_width,20);
	f.add(femaleComboBox);
	
	JLabel minAgeLabel = new JLabel("Minimum Age");
	minAgeLabel.setBounds(first_column_width + 50,25,first_column_width,20);
	f.add(minAgeLabel);
	final JTextField minAgeField = new JTextField();
	minAgeField.setBounds(first_column_width + 50,50,first_column_width,20);
	f.add(minAgeField);
	
	JLabel maxAgeLabel = new JLabel("Maximum Age");
	maxAgeLabel.setBounds(first_column_width + 50,75,first_column_width,20);
	f.add(maxAgeLabel);
	final JTextField maxAgeField = new JTextField();
	maxAgeField.setBounds(first_column_width + 50,100,first_column_width,20);
	f.add(maxAgeField);
	
	JLabel fatherLabel = new JLabel("Father (Optional)");
	fatherLabel.setBounds(first_column_width + 50,125,first_column_width,20);
	f.add(fatherLabel);
	final JTextField fatherField = new JTextField();
	fatherField.setBounds(first_column_width + 50,150,first_column_width,20);
	f.add(fatherField);
	
	JLabel motherLabel = new JLabel("Mother (Optional)");
	motherLabel.setBounds(first_column_width + 50,175,first_column_width,20);
	f.add(motherLabel);
	final JTextField motherField = new JTextField();
	motherField.setBounds(first_column_width + 50,200,first_column_width,20);
	f.add(motherField);
	
	JLabel deathLabel = new JLabel("How Long Dead (years) (optional)");
	deathLabel.setBounds(first_column_width + 50,225,first_column_width,20);
	f.add(deathLabel);
	final JTextField deathField = new JTextField();
	deathField.setBounds(first_column_width + 50,250,first_column_width,20);
	f.add(deathField);
	
	JLabel traitLabel = new JLabel("Mandatory Trait File Path(Optional)");
	traitLabel.setBounds(first_column_width + 50,275,first_column_width,20);
	f.add(traitLabel);
	final JTextField traitField = new JTextField();
	traitField.setBounds(first_column_width + 50,300,first_column_width,20);
	f.add(traitField);
	
	JLabel spouseLabel = new JLabel("Spouse (Optional)");
	spouseLabel.setBounds(first_column_width + 50,325,first_column_width,20);
	f.add(spouseLabel);
	final JTextField spouseField = new JTextField();
	spouseField.setBounds(first_column_width + 50,350,first_column_width,20);
	f.add(spouseField);
	
	JLabel marryLengthLabel = new JLabel("Marriage Length (years) (Optional)");
	marryLengthLabel.setBounds(first_column_width + 50,375,first_column_width,20);
	f.add(marryLengthLabel);
	final JTextField marryLengthField = new JTextField();
	marryLengthField.setBounds(first_column_width + 50,400,first_column_width,20);
	f.add(marryLengthField);
	
	JLabel authorLabel = new JLabel("Author");
	authorLabel.setBounds(first_column_width + 50,425,first_column_width,20);
	f.add(authorLabel);
	final JTextField authorField = new JTextField();
	authorField.setBounds(first_column_width + 50,450,first_column_width,20);
	f.add(authorField);
	
	JLabel titleListLabel = new JLabel("Title List File Path (Optional)");
	titleListLabel.setBounds(first_column_width + 50,475,first_column_width,20);
	f.add(titleListLabel);
	final JTextField titleListField = new JTextField();
	titleListField.setBounds(first_column_width + 50,500,first_column_width,20);
	f.add(titleListField);
	
	JLabel titleHistoryLabel = new JLabel("History Title File Path (Optional)");
	titleHistoryLabel.setBounds(first_column_width*2 + 100,25,first_column_width,20);
	f.add(titleHistoryLabel);
	final JTextField titleHistoryField = new JTextField();
	titleHistoryField.setBounds(first_column_width*2 + 100,50,first_column_width,20);
	f.add(titleHistoryField);
	
	JLabel liegeLabel = new JLabel("Liege (Optional)");
	liegeLabel.setBounds(first_column_width*2 + 100,75,first_column_width,20);
	f.add(liegeLabel);
	final JTextField liegeField = new JTextField();
	liegeField.setBounds(first_column_width*2 + 100,100,first_column_width,20);
	f.add(liegeField);
	
	JLabel titleLengthLabel = new JLabel("Title Length (Optional)");
	titleLengthLabel.setBounds(first_column_width*2 + 100,125,first_column_width,20);
	f.add(titleLengthLabel);
	final JTextField titleLengthField = new JTextField();
	titleLengthField.setBounds(first_column_width*2 + 100,150,first_column_width,20);
	f.add(titleLengthField);
	
	JLabel logLabel = new JLabel("Log");
	logLabel.setBounds(25, 525, first_column_width, 20);
	f.add(logLabel);
	JTextArea log = new JTextArea();
	log.setBounds(25, 550, 700, 150);
	f.add(log);
	
	JButton generateButton = new JButton("Generate Characters!");
	generateButton.setBounds(first_column_width*2 + 100, 500, first_column_width, 20);
	generateButton.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent e){  
			
			FileWriter fw = null;
			BufferedWriter bw = null;
			PrintWriter pw = null;
			
			FileWriter fw2 = null;
			BufferedWriter bw2 = null;
			PrintWriter pw2 = null;
			
			List<String> maleNames = null;
			List<String> femaleNames = null;
			List<String> dynasties = null;
			List<String> traits = null;
			List<String> titles = null;
			String name;
			String religion;
			String culture;
			String dynasty = "";
			int start;
			String id;
			int amount;
			int death = -1;
			String spouse;
			int marryLength = -1;
			int max_age;
			int min_age;
			int age;
			int game_start = 1254;
			int titleCount = 0;
			int titleLength = 0;
			String liege = "error";
			
			
			String father;
			String mother;
			String author;
			String female;
			Boolean rand_gender = false;
			
			//Checking the output file to see if it actually exists
			File outputFile = new File (outFileField.getText());
			File outputTitleFile = new File (titleHistoryField.getText());
			if (outputFile.exists())
			{
			log.append("Generating Characters...\n");
			
			//pulling information from the files/inputs
			
			//pull start number
			start = Integer.parseInt(startField.getText());
			//pull id
			id = idField.getText();
			//pull amount
			amount = Integer.parseInt(amountField.getText());
			//pull male names
				try
				{
					maleNames = readFile(maleNameField.getText());
				}
				catch (IOException err_i) {
					log.append("Error: Invalid Male Name List File Path\n");
				};
			//pull female names
				try
				{
					femaleNames = readFile(femaleNameField.getText());
				}
				catch (IOException err_i) {
					log.append("Error: Invalid Female Name List File Path\n");
				};
			
			//pull religion
			religion = religionTextField.getText();
			//pull culture
			culture = cultureField.getText();
			//pull dynasties
			if (!dynastyField.getText().equals(""))
			{
			try
				{
					dynasties = readFile(dynastyField.getText());
				}
				catch (IOException err_i) {
					log.append("Error: Invalid Dynasty List File Path\n");
					};
			}
			//pull female
			female = (String)femaleComboBox.getSelectedItem();
			if (female.equals("random")) rand_gender = true;
			//pull minimum age
			min_age = Integer.parseInt(minAgeField.getText());
			//max age
			max_age = Integer.parseInt(maxAgeField.getText());
			
			//father
			father = fatherField.getText();
			//mother
			mother = motherField.getText();
			//how long dead
			if (!deathField.getText().equals("")) death = Integer.parseInt(deathField.getText());
			//mandatory traits
			if (!traitField.getText().equals(""))
			{
				try
				{
					traits = readFile(traitField.getText());
				}
				catch (IOException err_i) {
					log.append("Error: Invalid Mandatory Trait List File Path\n");
					};
			}
			//spouse
			spouse = spouseField.getText();
			//marriage length
			if (!marryLengthField.getText().equals("")) marryLength = Integer.parseInt(marryLengthField.getText());
			//author
			author = authorField.getText();
			
			//pulling titles to give
			if (!titleListField.getText().equals(""))
			{
				try
				{
					titles = readFile(titleListField.getText());
				}
				catch (IOException err_i) {
					log.append("Error: Invalid Title List File Path\n");
					};
			}
			//pulling liege
			if (!liegeField.getText().equals("")) liege = liegeField.getText();
			//pulling title length
			if (!titleLengthField.getText().equals("")) titleLength = Integer.parseInt(titleLengthField.getText());
			
			//Okay we are done pulling from input, now to build the output.
		try { 
			fw = new FileWriter(outFileField.getText(), true);
			bw = new BufferedWriter(fw);
			pw = new PrintWriter(bw);
			
			DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");  
			LocalDateTime now = LocalDateTime.now();  
	
			pw.println("#Characters Generated at " + dtf.format(now) + " by " + author);
		
		
				for (int i = start; i < start+amount; i++)
				{
					//marking any pregenerated title
					if (!titleListField.getText().equals("") && titleCount < titles.size())
					{						
						pw.println("#" + titles.get(titleCount));
						titleCount++;
					}
					Random rand = new Random();
					if (!dynastyField.getText().equals("")) dynasty = dynasties.get(rand.nextInt(dynasties.size()));
					if (rand_gender)
					{
						int rand_int1 = rand.nextInt(2);
						if (rand_int1 == 1)	female = "yes";
						else female = "no";
					}
					if (female.equals("yes")) name = femaleNames.get(rand.nextInt(femaleNames.size()));
					else name = maleNames.get(rand.nextInt(maleNames.size()));
					age = min_age + rand.nextInt(max_age-min_age);
					
					//name, religion, culture, dynasty, gender
					pw.println(id + i + " = \n{\n name = \""+ name +"\"\n religion = \"" + religion + "\"\n culture = \"" + culture + "\"");
					if (!dynastyField.getText().equals("")) pw.println("dynasty = " + dynasty);
					pw.println("female = "+ female);
					
					//familial relation
					if (!father.equals("")) pw.println("father = " + father + "\n");
					if (!mother.equals("")) pw.println("mother = " + mother  + "\n");
					
					//traits
					if (!traitField.getText().equals(""))
					{
						for (int j = 0; j < traits.size(); j++)
						{
							pw.println("trait = " + traits.get(j) + "\n");
						}
					}
					
					//birthday!
					pw.println((game_start - age) + ".1.1 =\n{\n	birth = yes\n}\n");
					
					//marriage!
					if (!spouse.equals(""))
					{
						if (marryLength > -1)
						{
							pw.println((game_start-marryLength) + ".1.1 =\n{\n	add_spouse = " + spouse + "\n}\n");
						}
					}
					
					//death!
					if (death > -1) pw.println((game_start-death) + ".1.1 =\n{\n	death = yes \n}\n");
					
					//end of printing to the character list file!
					pw.println("}");
				}	
				
			} catch (IOException io) {}
			finally { //Close the files when done
				try {
					log.append("Closing files...\n");
				pw.close();
                bw.close();
                fw.close();
				} catch (IOException io) {}
			}
			if (!titleListField.getText().equals(""))
			{
				try
				{
					fw = new FileWriter(titleHistoryField.getText(), true);
					bw = new BufferedWriter(fw);
					pw = new PrintWriter(bw);
					DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");  
					LocalDateTime now = LocalDateTime.now();  
					pw.println("#Titles Generated at " + dtf.format(now) + " by " + author);
				
					//creating titles
					for (int i = 0; i < titles.size(); i++)
					{
							//building the title in the title history file
							pw.println(titles.get(i) + " = \n{");
							pw.println((game_start-titleLength) + ".1.1 =\n{");
							pw.println("holder = " + id + (i+start));
							if (!liegeField.getText().equals("")) pw.println("liege = " + liege);
							pw.println("}\n}");			
							titleCount++;
					}
				} catch (IOException io) {}
				finally { //Close files when done 
					try {
						log.append("Closing files...\n");
					pw.close();
					bw.close();
					fw.close();
					} catch (IOException io) {}
				}
			}
			startField.setText(Integer.toString(start + amount));
			log.append("Characters generated, start has been incremented!\n");
			}
			else //invalid output file
			{
				log.append("Error: Invalid Output File Path\n");
			}
			
        }  
    });
		
	f.add(generateButton);
	
    f.setSize(750,750);  
    f.setLayout(null);  
    f.setVisible(true);   
	f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);	
	
	
	
	String outFileName = "error";
	//Opening up Bufferreader to read from keyboard 
	/*
	FileWriter fw = null;
    BufferedWriter bw = null;
    PrintWriter pw = null;
	
	//Checks if that name corresponds to a file, then repeats until there is one
	File outputFile = new File (outFileName);
	
	
	//TEST CODE THROUGH THE CONSOLE
	//Will continue asking until you find a real file
	while (outputFile.exists() == false)
	{
		System.out.println("File " + outFileName + " not found, input new filename");
		outFileName = reader.readLine();
		outputFile = new File (outFileName);
		//C:\Users\mpjam\Documents\Paradox Interactive\Crusader Kings III\mod\godherja\history\characters\gh_canian.txt
		//If the filename is empty, exit the program
		if("".equals(outFileName))
		{
			System.out.println("Exiting program...");
			return;
		}
	}
	
	try
	{
		fw = new FileWriter(outFileName, true);		
        bw = new BufferedWriter(fw);
        pw = new PrintWriter(bw);
		int start = 0;
		String id;
		int amount = 0;
		
		String name;
		String religion;
		String culture;
		String dynasty;
		boolean rand_dynasty = false;
		boolean rand_gender = false;
		String gender;
		int max_age;
		int min_age;
		int age;
		int game_start = 1254;
		List<String> maleNames = new ArrayList<>();
		List<String> femaleNames = new ArrayList<>();
		List<String> dynasties = new ArrayList<>();
		
		
		System.out.println("Input the number of the first character you would like to generate!");
		start = Integer.parseInt(reader.readLine());
		System.out.println("Input the identifying string for the first character you would like to generate!");
		id = reader.readLine();
		System.out.println("How many characters would you like to generate?");
		amount = Integer.parseInt(reader.readLine());
		System.out.println("Please enter the desired religion here:");
		religion = reader.readLine();
		System.out.println("Please enter the desired culture here:");
		culture = reader.readLine();
		do
		{
			System.out.println("Input valid dynasties, if you input nothing, it will end:");
			dynasty = reader.readLine();
			if (!dynasty.equals("")) dynasties.add(dynasty);
		}
		while (!dynasty.equals(""));
		if ("".equals(dynasty)) rand_dynasty = true;
		System.out.println("Female yes/no (case sensitive), neither is random gender");
		gender = reader.readLine();
		if (!gender.equals("yes") && !gender.equals("no")) rand_gender=true;
		System.out.println("Input maximum age 0-100");
		max_age = Integer.parseInt(reader.readLine());
		System.out.println("Input minimum age 0-100");
		min_age = Integer.parseInt(reader.readLine());
		if (!gender.equals("yes"))
		{
			do 
			{
				System.out.println("Please input some appropriate male names, to stop entering names enter nothing");
				name = reader.readLine();
				if (!name.equals("")) maleNames.add(name);
			}
			while (!name.equals(""));
		}
		if (!gender.equals("no"))
		{
			do 
			{
				System.out.println("Please input some appropriate female names, to stop entering names enter nothing");
				name = reader.readLine();
				if (!name.equals("")) femaleNames.add(name);
			}
			while (!name.equals(""));
		}
		
		
		
		
		DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");  
		LocalDateTime now = LocalDateTime.now();  
		
		pw.println("#Characters Generated at " + dtf.format(now));
		
		for (int i = start; i < start+amount; i++)
		{
			Random rand = new Random();
			dynasty = dynasties.get(rand.nextInt(dynasties.size()));
			if (rand_gender)
			{
				int rand_int1 = rand.nextInt(2);
				if (rand_int1 == 1)	gender = "yes";
				else gender = "no";
			}
			if (gender.equals("yes")) name = femaleNames.get(rand.nextInt(dynasties.size()));
			else name = maleNames.get(rand.nextInt(dynasties.size()));
			age = min_age + rand.nextInt(max_age-min_age);
			
			//name, religion, culture, dynasty, gender
			pw.println(id + i + " = \n{\n name = \""+ name +"\"\n religion = \"" + religion + "\"\n culture = \"" + culture + "\"\n dynasty = " + dynasty +"\n female = "+ gender + "\n");
			
			//familial relation
			
			//birthday!
			pw.println ((game_start - age) + ".1.1 =\n{\n	birth = yes\n}\n}");
		
		}
		
		
	}
	finally {
            try {
                pw.close();
                bw.close();
                fw.close();
            } catch (IOException io) {// can't do anything
			}
            }
	*/
}
	static List<String> readFile(String filename) throws FileNotFoundException, IOException
	{
		File inf = new File(filename);
		String line;
		BufferedReader file_reader = new BufferedReader(new FileReader(inf));
		List<String> outputList = new ArrayList<>();
		while ((line=file_reader.readLine()) != null)
		{
			//debug print line pulled
			//System.out.println("line pulled from " + filename + " : " + line);
			outputList.add(line);
		}
		file_reader.close();
		return outputList;
	}		
}
