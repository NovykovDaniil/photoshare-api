from src.services import messages

def test_messages():
    assert messages.TAG_EXISTS == "Tag with such name exists"
    assert messages.TAG_CREATED == "Tag successfully created"
    assert messages.PHOTO_POSTED == "Photo successfully posted"
    assert messages.PHOTO_DOES_NOT_EXIST == "There is no photo with such ID"
    assert messages.PHOTO_DELETED == "Photo successfully deleted"
    assert messages.PHOTO_DESCRIPTION_EDITED == "Description successfully edited"
    assert messages.PHOTOS_SEARCHED == "Searched photos"
    assert messages.PHOTOS_NOT_FOUND == "There are no photos with such tag or keyword"
    assert messages.PHOTO_FOUND == "Photo successfully found"
    assert messages.PHOTO_TAG_ADDED == "Tags successfully added"
    assert messages.PHOTO_FILTER_ADDED == "Filter successfully added"
    assert messages.NO_FILTER == 'There are no such filter'
    assert messages.TOO_MANY_TAGS == 'You can not add more than 5 tags to photo'
    assert messages.COMMENT_CREATED == "Comment successfully created"
    assert messages.COMMENT_EDITED == "Comment successfully edited"
    assert messages.COMMENT_DOES_NOT_EXIST == "There is no comment with such ID"
    assert messages.COMMENT_DELETED == "Comment successfully deleted"
    assert messages.NO_COMMENTS == "There are no comments"
    assert messages.COMMENTS_FOUND == "Comments successfully found"
    assert messages.ACCOUNT_EXISTS == "Account already exists"
    assert messages.USERNAME_EXISTS == "Username already exists"
    assert messages.USER_CREATED == "User successfully created. Check your email for confirmation."
    assert messages.INVALID_EMAIL == "Invalid email"
    assert messages.NOT_CONFIRMED == "Email not confirmed"
    assert messages.INVALID_PASSWORD == "Invalid password"
    assert messages.INVALID_REFRESH_TOKEN == "Invalid refresh token"
    assert messages.VERIFICATION_ERROR == "Verification error"
    assert messages.EMAIL_ALREADY_CONFIRMED == "Your email is already confirmed"
    assert messages.EMAIL_CONFIRMED == "Email confirmed"
    assert messages.CHECK_EMAIL == "Check your email for confirmation."
    assert messages.RESET_CODE_CHECK == "Check your email with the reset code"
    assert messages.USER_NOT_FOUND == "User with such email was not found"
    assert messages.PASSWORD_CHANGED == "Password successfully changed"
    assert messages.WRONG_RESET_CODE == "Reset code is wrong"
    assert messages.SAME_PASSWORDS == "Passwords are the same"
    assert messages.WRONG_PASSWORD == "Wrong password"
    assert messages.NO_USERNAME == "There is no user with such username"
    assert messages.USER_FOUND == "User was successfully found"
    assert messages.USER_EDITED == "User bio was successfully edited"
    assert messages.NOT_YOUR_ACCOUNT == "It is not your account"
    assert messages.USER_ID_NOT_FOUND == 'There are no user with such id'
    assert messages.BANNED == "Your account has been banned"
    assert messages.NO_RECORD == "There is no record with such ID or it is not your record"
    assert messages.ONLY_IMGS == "You can only upload images"
    assert messages.NO_PHOTO_OR_NOT_YOUR == "There is no photo with such ID or it is not your photo"
    assert messages.NO_PHOTO == "There is no photo with such ID"
    assert messages.NO_PHOTO_URL == "There is no photo with such image url"
    assert messages.USER_ACTIVE_CHANGED == "User active status was successfully changed"
    assert messages.LOGGED_OUT == 'Logged out successfully.'
    assert messages.PHOTO_ESTIMATED == "Photo successfully estimated"
    assert messages.ESTIMATE_EXISTS_OR_YOUR_PHOTO == "Does the estimate exist or do you want to estimate your photo"
    assert messages.ESTIMATES_FOUND == "Estimates were successfully found"
    assert messages.ESTIMATES_NOT_FOUND == "There are no estimates"
    assert messages.NO_ESTIMATE == "There is no estimate with such ID"
    assert messages.ESTIMATE_DELETED == "Estimate was successfully deleted"
    assert messages.STORY_CREATED == 'Story successfully created'
    assert messages.ONLY_VIDEO == 'You can upload only videos'
    assert messages.NO_STORY == 'There are no story with such id'
    assert messages.STORY_FOUND == 'Story was successfully found'
    assert messages.STORY_DELETED == 'Story was successfully deleted'
    assert messages.NO_STORIES == 'Unfortunately, not one user from your subscriptions has not posted the story'
    assert messages.STORIES_FOUND == 'Stories was successfully found'
    assert messages.STORY_NOT_AVALIABLE == 'Story is already inaccessible'
    assert messages.SUBSCRIBED == 'You have successfully subscribed'
    assert messages.SUBS_FOUND == 'Subscriptions successfully found'
    assert messages.SUBS_NOT_FOUND == 'You haven\'t subscribed to anyone'
    assert messages.NO_SUB == 'You were not subscribed to user with such ID'
    assert messages.SUB_DELETED == 'You have successfully unsubscribed from the user'
    assert messages.STORY_NOT_YOUR == 'It is not your story'
    assert messages.AUTHOR_ID_NOT_FOUND == 'Author with such is was not found'
    assert messages.ADMIN_PERMISSIONS == ['admin']
    assert messages.MODERATOR_PERMISSIONS == ['admin', 'moderator']
    assert messages.NO_PERMISSIONS == 'You do not have access to this route'
    assert messages.QR_SERVICE_EMAIL == 'qr@service.email'
