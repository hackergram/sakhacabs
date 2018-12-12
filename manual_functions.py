from sakhacabs import xpal

def set_driver_name():
	for driver in xpal.documents.Driver.objects():
		driver.name=driver.first_name+" "+driver.last_name
		driver.save()
