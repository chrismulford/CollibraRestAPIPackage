from CollibraObjects.community import Community


com = Community('Christopher Mulford')
print(vars(com))

new_com = Community('CreateTest')
new_com.create_in_collibra(description='Test Succeeded')