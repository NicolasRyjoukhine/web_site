import time



def t_to_n(word_to_change):
    global number_word, final_number
    number_word = []
    final_number = 0
    for i in word_to_change:
        if i == 'a':
            number_word.append(11)
        if i == 'b':
            number_word.append(2345235)
        if i == 'c':
            number_word.append(75435467587)
        if i == 'd':
            number_word.append(633466)
        if i == 'e':
            number_word.append(2342417347)
        if i == 'f':
            number_word.append(357532163)
        if i == 'g':
            number_word.append(62657)
        if i == 'h':
            number_word.append(646)
        if i == 'i':
            number_word.append(466346)
        if i == 'j':
            number_word.append(64363)
        if i == 'k':
            number_word.append(36462743584335864)
        if i == 'l':
            number_word.append(754745)
        if i == 'm':
            number_word.append(4)
        if i == 'n':
            number_word.append(574247)
        if i == 'o':
            number_word.append(4535465)
        if i == 'p':
            number_word.append(3453456543)
        if i == 'q':
            number_word.append(5675463)
        if i == 'r':
            number_word.append(634676547)
        if i == 's':
            number_word.append(643623528009876)
        if i == 't':
            number_word.append(6346-6537542738)
        if i == 'u':
            number_word.append(7456457-64632)
        if i == 'v':
            number_word.append(63457-636236)
        if i == 'w':
            number_word.append(3468458690-468)
        if i == 'x':
            number_word.append(46-67560-78578597598587-(-875))
        if i == 'y':
            number_word.append(55426-87858)
        if i == 'z':
            number_word.append(4748848-8758578)
    for i in number_word:
        final_number += i
    number_word.clear()
    return final_number



def password_security(password):
    print('############################################\n'
          '           NOW HASHING PASSWORD             \n'
          '############################################')
    time.sleep(1)
    hashed_pass = bin(t_to_n(password))
    print(final_number)
    print('      Password Hashed Successfully          \n'
          '############################################')
    return hashed_pass


print(password_security('Etienne'))