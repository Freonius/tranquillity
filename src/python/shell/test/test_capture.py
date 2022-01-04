def test_capture():
    from ..tranquillity.shell import Capture
    what_the_hell_did_I_say = ''
    with Capture() as c:
        print('You never listen!')
        what_the_hell_did_I_say = str(c)
    assert what_the_hell_did_I_say == 'You never listen!'
