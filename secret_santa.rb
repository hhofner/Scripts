require 'mail'
# Secret Santa 

# names of all participants
friends       = Array.new
participants  = Array.new
secret_santas = Array.new
emails        = Hash.new

# secret santa assignments
ss_mappings = Hash.new

name = 'temp'
email = 'temp'
print 'Enter Name and Email: '
while user_input = gets.chomp 
	splitted_input = Array.new
	case user_input
	when "end"
		puts "Sending Secret Santas!"
		break
	when ""
		puts "Sending Secret Santas!"
		break
	else
	    splitted_input = user_input.split('-') 
	    friends.push(splitted_input[0])
		participants.push(splitted_input[0])
		secret_santas.push(splitted_input[0])
		name = splitted_input[0]
	    email = splitted_input[1]
	    emails["#{name}"] = "#{email}"
	end
end

if (friends.length < 3)
	puts "only allows for 4 or more people"
else
	# randomize and check if key is not equal to value
	size = friends.length
	while ss_mappings.length < size
		# make copy of friends array
	    ss = secret_santas.sample
		ff = friends.sample
		if ss == ff
			puts 'Mismatch'
		else
			ss_mappings["#{ss}"] = ff
			secret_santas.delete("#{ss}")
			friends.delete("#{ff}")
		end
	end
end
#puts ss_mappings

options = { :address              => '',
	        :port                 => 7,
			:domain               => 'your.host.name',
			:user_name            => 'MY_USER_NAME',
			:password             => 'MY_PASSWORD',
			:authentication       => 'plain',
			:enable_starttls_auto => true }
Mail.defaults do
	  delivery_method :smtp, options
end

# write to file
for friend in participants do
	File.open("body.txt", "w") do |f|
		f.print("Thank you for taking part in Secret Santa!\n")
		f.puts("\n")
		f.puts("Remember to keep this secret...")
		f.puts("You are secret santa for...\n")
		f.puts("\n")
		f.puts("\n")
		f.puts "#{ss_mappings["#{friend}"]} !"
	end
	mail = Mail.new do	    
	    to emails["#{friend}"] 
		#to 'B1401489@gl.aiu.ac.jp'
		from 'your_email@site.com'
	    subject '~* SECRET SANTA *~'
	    body File.read('body.txt')	
	end
mail.deliver!
end
