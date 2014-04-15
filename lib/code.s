# Exit
exit:
	li 		$v0, 10 				# Preparing for exit system call
	syscall

# Sub routine for printing integer input
print_integer:
	li		$v0, 1 					# Preparing the system for the print_integer system call
	syscall
	jr		$ra

# Sub routine for printing sting input
print_string:
	li		$v0, 4 					# Preparing the system for the print_string system call
	syscall
	jr		$ra

# Sub routine for accepting integer input
input_integer:
	li		$v0, 5					# Prepare the system for input_integer system call
	syscall				
	jr		$ra						# Return to the callee

