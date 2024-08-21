# importing module 
from bs4 import BeautifulSoup 
  
markup = """ 
  
<!DOCTYPE> 
<html> 
  <head><title>Example</title></head> 
  <body> 
  <div id="parent"> 
    
<p> 
    This is child of div with id = "parent". 
    <span>Child of "P"</span> 
  </p> 
  
  <div> 
  Another Child of div with id = "parent". 
  </div> 
  </div> 
  
    
<p> 
  Piyush 
  </p> 
  
                     
  </body> 
</html> 
"""
  
# parsering string to HTML 
soup = BeautifulSoup(markup, 'html.parser') 
  
# finding tag whose child to be deleted 
div_bs4 = soup.find('div') 
  
# delete the child element 
div_bs4.decompose() 
  
print(soup.prettify()) 