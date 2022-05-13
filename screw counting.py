print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
contents = []
while True:
    try:
        line = input()
    except EOFError:
        break
    contents.append(line)
    
print(contents)

screw_count = {
4136:4,
4132:2,
4143:4,
4164:4,
4081:5,
4080:4,
4101:4
}

final_values = []
for values in contents:
    multipler = int(values.split('x')[0])
    part_number = int(values.split('x')[1].replace(" ", ""))
    multipler_stored = screw_count[part_number]
    final_values.append(multipler*multipler_stored)

print(sum(final_values))