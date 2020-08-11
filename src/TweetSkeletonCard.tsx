import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import Skeleton from "@material-ui/lab/Skeleton";
import React from "react";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      maxWidth: 600,
      backgroundColor: theme.palette.background.paper,
    },
  })
);

export const TweetSkeletonCard = () => {
  const classes = useStyles();

  const avatar = <Skeleton variant="circle" width={40} height={40} />;

  return (
    <Card className={classes.root}>
      <CardHeader align="left" avatar={avatar} />
      <CardContent>
        <Skeleton variant="text" />
        <Skeleton variant="text" />
        <Skeleton variant="text" />
      </CardContent>
    </Card>
  );
};
