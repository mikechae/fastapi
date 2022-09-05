from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, database, models, oauth2 
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.get("/vote", status_code=status.HTTP_201_CREATED) 
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends
(oauth2.get_current_user)):
   
   #checks to see if like exists for this post by current user
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        #does vote already exist for this post and current user
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f"User{current_user.id} has already liked post {vote.post_id}")
        #if it doesnt, set two properties in "vote" postgres table
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id) 
        db.add(new_vote)
        db.commit()
        return {"message": "vote successful"}   
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "vote deletion successful"}