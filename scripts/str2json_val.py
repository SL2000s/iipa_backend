def multiline_input():
   contents = []
   while True:
      try:
         line = input()
      except EOFError:
         break
      contents.append(line)
   ip = '\n'.join(contents)
   return ip

def str2json_val(s):
   s = s.strip('\n')
   s = s.replace('"', '\\"')
   s = s.replace('\n', '\\n')
   return s


if __name__ == '__main__':
   ip = multiline_input()
   json_val = str2json_val(ip)
   print(json_val)
