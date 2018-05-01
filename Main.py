
import requests
import queue






def findUrl(page, beginning):

    page = page.replace(" ", "")

    start = page.find("href=", beginning)
    end = page.find("\"", start + 6)
    end_alt = page.find("'", start + 6)
    #end_alt2 = page.find("asfsdgsdfgsdfgsdfgsdfgsdfg", start + 8)

    # print(start)
    # print(end)
    # print(end_alt)
    # #print(end_alt2)


    if start > 0:
        if end > start:
            if end < end_alt:
                final_end = end
            else:
                final_end = end_alt
        else:
            if end_alt > start:
                final_end = end_alt
            else:
                final_end = -1

        return page[start + 6: final_end], final_end

    else:

        return "", -1



    # print(start)
    # print(end)
    # print(end_alt)
    # #print(end_alt2)
    # print(final_end)


def process_one_url(url, q):

    r = requests.get(url)

    print(str(r.content))

    cont = True
    pos = 0

    ignore_endings = {".jpg", ".png", ".gif", ".ico", ".css", ".js"}
    ignore_matches = {"twitter.com", "facebook.com", "youtube.com", "instagram.com", "/auth/"}
    required_text = "segodnya.ua"

    while cont:

        txt, c = findUrl(str(r.content), pos)
        #print(txt)
        #print(c)

        add = False

        if required_text in txt:

            add = True

            for m in ignore_endings:
                if txt.endswith(m):
                    add = False

            for m in ignore_matches:
                if m in txt:
                    add = False

        if add:
            print(txt)
            q.put(txt)

        pos = c

        if c < 0:
            cont = False




def load_from_root(url, limit):

    q = queue.Queue()
    q.put(url)
    done = []

    do_continue = True
    counter = 0;

    while do_continue:

        u = q.get()

        if u in done:
            print("ignored")
        else:
            process_one_url(u, q)
            done.append(u)
            print(len(done))

        s = q.qsize()
        print(s)
        if s < 1:
            do_continue = False

        if counter >= limit:
            do_continue = False

        counter += 1


load_from_root("https://www.segodnya.ua/", 10)