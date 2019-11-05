"""Google Chrome Bookmark File to Web Page Converter

This script allows the user to convert Google Chrome bookmarks they have
saved on their machine to a HTML file that can be posted as a standalone
page of links (with table of contents) on their Github Pages website.

INPUTS:
    1) bookmarks.json (Google Chrome bookmarks file, saved on a Windows
            system under C:/Users/___/AppData/Local/Google/Chrome/User Data/
            Default as "Bookmarks" without file extension)
    2) bookmarks.html (Google Chrome bookmarks file, created by exporting
            bookmarks directly out of Chrome, using Bookmark Manager)

OUTPUTS:
    1) folders.txt (text file with hierarchical list of bookmark folder names)
            (intermediate step)
    2) toc.html (HTML unordered list of bookmark folder names with links to
            corresponding sections of the page) (intermediate step)
    3) links_with_bookmarks.html (bookmarks.html file above, with ID= attributes
            added to section headings to allow for the table of contents to
            function) (intermediate step)
    4) links.html (toc.html file above, with contents of the
            links_with_bookmarks file above appended)

NOTES:
    1) The following (and/or other) CSS styles can be saved separately
            (or incorporated into the HTML code through additional scripting):
        li {
            font-weight: bold;
            list-style-type: disc;
        }

        h3 a{
            float: right;
            font-size: 15px;
        }
"""
import json
import os

def by_key(item):
    return item[0]

def print_folders(lst, f_handle, level=0):
    '''Print hierarchy of bookmark folder names to file.'''
    # loop over folders
    for d in lst:
        # loop over properties of folder (name, type, children, etc.)
        # dictionary is first sorted by key in reverse chronological order,
        # so that the folder name is printed first, followed by children's names
        for k, v in sorted(d.items(), key=by_key, reverse=True):
            if v == 'folder':
                print(' '*level*5 + d['name'], file=f_handle)
            elif k == 'children':
                print_folders(v, f_handle, level=level+1)

def print_toc(f_handle, add_front_matter=True):
    '''Read hierarchy of folder names and create HTML unordered list with same
    hierarchy.
    '''
    with open("folders.txt", "r") as f:
        lines = f.readlines()
        #first add correct Jekyll layout to the page's front-matter.
        if add_front_matter:
            print('---', file=f_handle)
            print('layout: page', file=f_handle)
            print('title: Links', file=f_handle)
            print('---', file=f_handle)
        print('<ul>', file=f_handle)
        for idx, line in enumerate(lines):
            if idx == len(lines)-1:
                break
            else:
                line = line.rstrip('\n')
                n_lead_spaces = len(line) - len(line.strip(' '))
                n_lead_spaces_next_line = len(lines[idx+1]) \
                    - len(lines[idx+1].strip(' '))
                n_lead_spaces_to_print = int(n_lead_spaces/5)+1

                if n_lead_spaces < (n_lead_spaces_next_line):
                    print(' '*n_lead_spaces_to_print,
                        f"""<li><a href="#{line.lstrip(' ')}">""",
                        line.lstrip(' '),'</a>',sep='', file=f_handle)
                    print(' '*n_lead_spaces_to_print,
                        f"""<ul>""",sep='', file=f_handle)
                elif n_lead_spaces == n_lead_spaces_next_line:
                    print(' '*n_lead_spaces_to_print,
                        f"""<li><a href="#{line.lstrip(' ')}">""",
                        line.lstrip(' '),'</a></li>',sep='', file=f_handle)
                elif n_lead_spaces > n_lead_spaces_next_line:
                    print(' '*n_lead_spaces_to_print,
                        f"""<li><a href="#{line.lstrip(' ')}">""",
                        line.lstrip(' '),'</a></li>',sep='', file=f_handle)
                    print(' '*n_lead_spaces_to_print,'</ul>',sep='',
                        file=f_handle)
                    print(' '*n_lead_spaces_to_print,'</li>',sep='',
                        file=f_handle)
        print('</ul>', file=f_handle)

def create_bookmarks(f_handle):
    '''Read links html source file and add ID= tags to section headings to
    allow for the table of contents to function, as well as links to top of page
    next to every heading.
    '''
    with open("bookmarks.html","r") as inf:
        #skip the first 7 lines of bookmarks file
        for _ in range(7):
            next(inf)
        line = inf.readline()
        while line:
            if line.lstrip().startswith("<DT><H3 "):
                id_str = ''.join(line.split('<')[:-1])
                id_str = ''.join(id_str.split('>')[-1])
                print(line.replace("<DT><H3 ",f"""<DT><H3 ID="{id_str}" """)
                    .replace("</H3>",""" <A HREF="#top">Back to Top</A></H3>"""),
                    file=f_handle)
            else:
                print(line, file=f_handle)
            line = inf.readline()

def merge_htmls():
    '''Append contents of the actual links file to the TOC file.'''
    with open("links_with_bookmarks.html","r") as links:
        with open("toc.html","a") as toc:
            for line in links:
                toc.write(line)
    os.rename('toc.html','links.html')

def main():
    with open("bookmarks.json", "r") as bks:
        books = json.load(bks)
    with open("folders.txt", "a") as f:
        print_folders(books['roots']['other']['children'], f)
    with open("toc.html","a") as toc:
        print_toc(toc)
    with open("links_with_bookmarks.html","a") as outf:
        create_bookmarks(outf)
    merge_htmls()

if __name__ == '__main__':
    main()
