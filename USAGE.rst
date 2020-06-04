=====
Usage
=====

To use outpost24lib in a project:

.. code-block:: python

    from outpost24hiablib import Outpost24
    op24lib = Outpost24(url, token)


    # Working with users and usergroups

	# enumerate users in Outpost24 HIAB
	users = op24lib.get_users()
	for user in users:
		print(user.vcusername)

    # enumerate usergroups in Outpost24 HIAB
	groups = op24lib.get_usergroups()
	for group in groups:
		print(group.vcname)
	
	# create a user
	user = op24lib.create_user(FIRST_NAME,
								LAST_NAME,
								EMAIL,
								PHONENUMBER,
								COUNTRY,
								USERNAME,
								PASSWORD,
								usergrouplist = [USERGROUP1_OBJECT],
								targetlist = [TARGET1_OBJECT],
								scannerlist = [SCANNER1_OBJECT])
	
	# delete users
	isdeleted = op24lib.delete_users([USER_OBJECT])
	
	# Working with scanners
	
	# enumerate scanners in Outpost24 HIAB
	scanners = op24lib.get_scanners()
	
	# Working with targets and targetgroups
	
	# enumerate targetgroups in Outpost24 HIAB
	targetgroups = op24lib.get_targetgroups()
	for targetgroup in targetgroups:
		print(targetgroup.name)
	
	# enumerate targets
	targets = op24lib.get_targets()
	for target in targets:
		print(target.hostname)
	
	# create target
	targetlist = op24lib.create_targets([IPADDRESS1, IPADDRESS2, HOSTNAME1, HOSTNAME2],
										TARGETGROUP_OBJECT,
										DNSLOOKUP = True,
										SCANNER=SCANNER_OBJECT,
										CUSTOM0 = STRING,
										CUSTOM1 = STRING,
										CUSTOM2 = STRING,
										CUSTOM3 = STRING,
										CUSTOM4 = STRING,
										CUSTOM5 = STRING)
										
	# delete targets
	isdeleted = op24lib.delete_targets([TARGET_OBJECT])
	
	# create targetgroup
	targetgroup = op24lib.create_targetgroup(TARGETGROUP_NAME)
	
	# delete targetgroups
	isdeleted = op24lib.delete_targetgroups([TARGETGROUP_OBJECT])
	
