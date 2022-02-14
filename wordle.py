"""Wordle solver"""
import math


def filter_answers_green(my_list: list[str], letter: str, index: int) -> list[str]:
    """Return list of answers with given letter at position index"""
    filtered = []
    for answer in my_list:
        if answer[index] == letter:
            filtered.append(answer)
    return filtered


def filter_answers_yellow(my_list: list[str], letter: str, index: int) -> list[str]:
    """Return list of answers containing given letter not at position index"""
    filtered = []
    for answer in my_list:
        if letter in answer and answer[index] != letter:
            filtered.append(answer)
    return filtered


def filter_answers_grey(my_list: list[str], letter: str) -> list[str]:
    """Return list of answers without given letter"""
    return [answer for answer in my_list if letter not in answer]


def return_possible_answers(my_list: list[str], word: str, feedback: str) -> list[str]:
    """Returns list of possible answers based on feedback"""
    filtered = my_list
    for j in range(5):
        if feedback[j] == '_':
            filtered = filter_answers_grey(filtered, word[j])
        elif feedback[j] == 'Y':
            filtered = filter_answers_yellow(filtered, word[j], j)
        elif feedback[j] == 'G':
            filtered = filter_answers_green(filtered, word[j], j)
        else:
            return []
    return filtered


def calculate_expected_information(feedback_prob: dict[str, float]) -> float:
    """Calculate the expected information in bits for given guess"""
    expected_info = 0
    for ind in feedback_prob:
        expected_info += feedback_prob[ind] * (-math.log2(feedback_prob[ind]))
    return expected_info


def return_feedback_for_word_given_guess(my_word: str, guess: str) -> str:
    """Return feedback"""
    my_feedback = ''
    for i in range(5):
        if my_word[i] == guess[i]:
            my_feedback += 'G'
        elif guess[i] in my_word:
            my_feedback += 'Y'
        else:
            my_feedback += '_'
    return my_feedback


def get_probability_feedback_sets(my_list: list[str], word: str) -> dict[str, float]:
    """Store proportion of how many words in allowed belong to each feedback set in dict"""
    feedback_information = {}
    for string in my_list:
        index = return_feedback_for_word_given_guess(string, word)
        if index in feedback_information:
            feedback_information[index] += 1
        else:
            feedback_information[index] = 1
    for i in feedback_information:
        feedback_information[i] = feedback_information[i] / len(my_list)

    return feedback_information


def get_best_word(my_list: list[str]) -> str:
    """Return the best possible guess"""
    if len(my_list) == 1:
        return my_list[0]
    max_info = (allowed_guesses[0], 0)
    for w in allowed_guesses:
        probabilities = get_probability_feedback_sets(possible, w)
        info = calculate_expected_information(probabilities)
        if info > 5.7:
            print(w + ': ' + str(info))
        if info > max_info[1]:
            max_info = (w, info)
    return max_info[0]


if __name__ == "__main__":
    with open('wordle-allowed-guesses.txt') as file:
        allowed_guesses = [line.rstrip() for line in file]
    with open('wordle-answers-alphabetical.txt') as file:
        allowed_answers = [line.rstrip() for line in file]
    allowed_guesses.extend(allowed_answers)

    possible = allowed_answers
    for i in range(6):
        best_word = get_best_word(possible)
        print('Best word: ' + best_word)
        print('Enter tried word: ')
        word = input().lower()
        print('Enter wordle feedback (letter absent = _, letter correct = G, letter present = Y):')
        feedback = input()
        possible = return_possible_answers(possible, word, feedback)

        print(possible)
    print('Out of tries')
